import time
from datetime import datetime

# Medicine Intake Alarm
# Reminder times are entered by the user.
# Confirm them against the doctor's prescription.

medicines = [
    {
        "name": "Samparaz D 40",
        "times": ["08:15"],
        "dose": "As prescribed by doctor"
    },
    {
        "name": "Rapitus",
        "times": ["11:00", "16:30"],
        "dose": "As prescribed by doctor"
    },
    {
        "name": "Pantop D",
        "times": ["20:30"],
        "dose": "As prescribed by doctor"
    },
    {
        "name": "Dolo",
        "times": ["21:00"],
        "dose": "As prescribed by doctor"
    },
    {
        "name": "Azithromycin",
        "times": ["22:30"],
        "dose": "As prescribed by doctor"
    }
]

print("=" * 40)
print("       MEDICINE INTAKE ALARM")
print("=" * 40)

print("\nYour medicine schedule:")
for medicine in medicines:
    times = ", ".join(medicine["times"])
    print(f'{medicine["name"]}: {times}')

print("\nAlarm is running.")
print("Keep this program open for reminders.")
print("Press Ctrl+C to stop.\n")

# Stores reminders already shown today
reminders_shown = set()
current_date = datetime.now().date()

try:
    while True:
        now = datetime.now()
        today = now.date()
        current_time = now.strftime("%H:%M")

        # Reset daily reminder history
        if today != current_date:
            reminders_shown.clear()
            current_date = today

        for medicine in medicines:
            for alarm_time in medicine["times"]:
                reminder_id = (
                    today,
                    medicine["name"],
                    alarm_time
                )

                if (
                    current_time == alarm_time
                    and reminder_id not in reminders_shown
                ):
                    print("\n" + "!" * 40)
                    print("          MEDICINE REMINDER")
                    print("!" * 40)
                    print("Medicine:", medicine["name"])
                    print("Scheduled time:", alarm_time)
                    print("Instruction:", medicine["dose"])
                    print("Check your prescription before taking it.")
                    print("!" * 40 + "\n")

                    print("\a", end="", flush=True)
                    reminders_shown.add(reminder_id)

        time.sleep(5)

except KeyboardInterrupt:
    print("\nMedicine alarm stopped.")