import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

FILE_NAME = "medicines.json"

medicines = [
    {"name": "Samparaz D 40", "times": ["08:15"]},
    {"name": "Rapitus", "times": ["11:00", "16:30"]},
    {"name": "Pantop D", "times": ["20:30"]},
    {"name": "Dolo", "times": ["21:00"]},
    {"name": "Azithromycin", "times": ["22:30"]}
]

reminders_shown = set()


def save_medicines():
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(medicines, file, indent=4)


def load_medicines():
    global medicines
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                data = json.load(file)
            if isinstance(data, list):
                medicines = data
        except (json.JSONDecodeError, OSError):
            messagebox.showwarning(
                "File Warning",
                "Saved file could not be read. Using default medicines."
            )


def refresh_table():
    for item in table.get_children():
        table.delete(item)

    for medicine in medicines:
        for alarm_time in medicine["times"]:
            table.insert(
                "", "end",
                values=(medicine["name"], alarm_time, "Scheduled")
            )


def add_medicine():
    name = name_entry.get().strip()
    alarm_time = time_entry.get().strip()

    if not name:
        messagebox.showerror("Missing Name", "Medicine ka naam enter karo.")
        return

    try:
        alarm_time = alarm_time.strip()
        parts = alarm_time.split(":")

        if len(parts) != 2:
            raise ValueError

        hour = int(parts[0])
        minute = int(parts[1])

        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError

        alarm_time = f"{hour:02d}:{minute:02d}"

    except ValueError:
        messagebox.showerror(
            "Invalid Time",
            "Time 24-hour format mein likho, jaise 08:30 ya 16:30."
        )
        return

    if not name:
        messagebox.showerror("Missing Name", "Medicine ka naam enter karo.")
        return

    existing = next(
        (m for m in medicines
         if m["name"].casefold() == name.casefold()),
        None
    )

    if existing:
        if alarm_time in existing["times"]:
            messagebox.showinfo(
                "Already Added", "Yeh medicine aur time pehle se added hain."
            )
            return
        existing["times"].append(alarm_time)
        existing["times"].sort()
    else:
        medicines.append({"name": name, "times": [alarm_time]})

    save_medicines()
    refresh_table()
    name_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Medicine reminder add aur save ho gaya.")


def delete_medicine():
    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Select Entry", "Delete karne ke liye table mein entry select karo."
        )
        return

    values = table.item(selected[0], "values")
    name, alarm_time = values[0], values[1]

    if not messagebox.askyesno(
        "Confirm Delete",
        f"{name} ka {alarm_time} reminder delete karna hai?"
    ):
        return

    for medicine in medicines:
        if medicine["name"] == name and alarm_time in medicine["times"]:
            medicine["times"].remove(alarm_time)
            break

    medicines[:] = [m for m in medicines if m["times"]]
    save_medicines()
    refresh_table()


def test_reminder():
    selected = table.selection()
    if not selected:
        messagebox.showwarning("Select Medicine", "Pehle ek entry select karo.")
        return

    name, alarm_time, _ = table.item(selected[0], "values")
    messagebox.showinfo(
        "Medicine Reminder",
        f"Medicine: {name}\nTime: {alarm_time}\n\n"
        "Doctor ki prescription check karo."
    )


def update_clock():
    now = datetime.now()
    clock_label.config(text="Current time: " + now.strftime("%I:%M:%S %p"))

    today = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M")

    for medicine in medicines:
        for alarm_time in medicine["times"]:
            reminder_id = (today, medicine["name"], alarm_time)

            if current_time == alarm_time and reminder_id not in reminders_shown:
                reminders_shown.add(reminder_id)
                root.bell()
                messagebox.showinfo(
                    "Medicine Reminder",
                    f"Medicine: {medicine['name']}\n"
                    f"Scheduled time: {alarm_time}\n\n"
                    "Prescription check karna na bhoolen."
                )

    root.after(1000, update_clock)


load_medicines()

root = tk.Tk()
root.title("Medicine Intake Alarm")
root.geometry("760x650")
root.configure(bg="#eef3f8")

tk.Label(
    root, text="MEDICINE INTAKE ALARM",
    font=("Arial", 22, "bold"), bg="#eef3f8", fg="#174a7e"
).pack(pady=(15, 5))

clock_label = tk.Label(root, font=("Arial", 12, "bold"), bg="#eef3f8")
clock_label.pack(pady=5)

table = ttk.Treeview(
    root, columns=("medicine", "time", "status"),
    show="headings", height=9
)

table.heading("medicine", text="Medicine")
table.heading("time", text="Reminder Time")
table.heading("status", text="Status")
table.column("medicine", width=270)
table.column("time", width=160, anchor="center")
table.column("status", width=180, anchor="center")
table.pack(padx=20, pady=10, fill="x")

refresh_table()

form = tk.LabelFrame(
    root, text="Add Medicine", font=("Arial", 11, "bold"),
    bg="#eef3f8", padx=12, pady=10
)
form.pack(padx=20, pady=8, fill="x")

tk.Label(form, text="Medicine name:", bg="#eef3f8").grid(
    row=0, column=0, padx=5, pady=5, sticky="w"
)
name_entry = tk.Entry(form, width=25)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(form, text="Time (HH:MM):", bg="#eef3f8").grid(
    row=1, column=0, padx=5, pady=5, sticky="w"
)
time_entry = tk.Entry(form, width=25)
time_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Button(
    form, text="Add Medicine", command=add_medicine,
    bg="#2471a3", fg="white", width=18
).grid(row=0, column=2, rowspan=2, padx=12)

buttons = tk.Frame(root, bg="#eef3f8")
buttons.pack(pady=12)

tk.Button(
    buttons, text="Test Reminder", command=test_reminder,
    bg="#2471a3", fg="white", width=16
).grid(row=0, column=0, padx=6)

tk.Button(
    buttons, text="Delete Selected", command=delete_medicine,
    bg="#b03a2e", fg="white", width=16
).grid(row=0, column=1, padx=6)

tk.Label(
    root, text="Keep the app open for reminders.",
    bg="#eef3f8", fg="#555555"
).pack(pady=5)

root.after(1000, update_clock)
root.mainloop()