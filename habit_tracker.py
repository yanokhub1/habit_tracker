import json
from datetime import date
from pathlib import Path


FILE = Path(__file__).parent / "habits.json"


def load_data():
    if not FILE.exists():
        return [], [], "", {}, {}

    with FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return (
        data.get("habits", []),
        data.get("completed", []),
        data.get("last_date", ""),
        data.get("streaks", {}),
        data.get("history", {})
    )


def save_data():
    data = {
        "habits": habits,
        "completed": completed,
        "last_date": last_date,
        "streaks": streaks,
        "history": history
    }

    with FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


habits, completed, last_date, streaks, history = load_data()


today = str(date.today())


if last_date != today:
    for habit in habits:
        if habit not in completed:
            streaks[habit] = 0

    completed = []
    last_date = today
    save_data()


def show_habits():
    print("\n--- YOUR HABITS ---")

    if not habits:
        print("No habits yet.")
        return

    for number, habit in enumerate(habits, start=1):
        status = "DONE" if habit in completed else "NOT DONE"
        print(f"{number}. {habit} - {status}")


def mark_completed():
    show_habits()

    if not habits:
        return

    try:
        number = int(input("\nEnter habit number: "))

        if number < 1 or number > len(habits):
            print("Invalid number.")
            return

        habit = habits[number - 1]

        if habit in completed:
            print("Already completed!")
        else:
            completed.append(habit)
            streaks[habit] = streaks.get(habit, 0) + 1

            if today not in history:
                history[today] = []

            if habit not in history[today]:
                history[today].append(habit)

            save_data()

            print("Habit completed!")
            print(f"Current streak: {streaks[habit]} day(s)")

    except ValueError:
        print("Please enter a valid number.")


def show_calendar():
    print("\n--- HABIT CALENDAR ---")

    if not history:
        print("No completed habits yet.")
        return

    for day in sorted(history):
        print(f"\n{day}")

        for habit in history[day]:
            print(f"  [DONE] {habit}")


def show_statistics():
    total = len(habits)
    done = len(completed)

    print("\n--- STATISTICS ---")
    print(f"Total habits: {total}")
    print(f"Completed: {done}")

    if total > 0:
        progress = done / total * 100
        print(f"Progress: {progress:.1f}%")
    else:
        print("Progress: 0%")

    print("\n--- STREAKS ---")

    for habit in habits:
        print(f"{habit}: {streaks.get(habit, 0)} day(s)")


def add_habit():
    name = input("\nEnter new habit: ").strip()

    if not name:
        print("Habit name cannot be empty.")
        return

    if name in habits:
        print("This habit already exists.")
        return

    habits.append(name)
    streaks[name] = 0
    save_data()

    print("Habit added!")


def edit_habit():
    show_habits()

    if not habits:
        return

    try:
        number = int(input("\nEnter habit number to edit: "))

        if number < 1 or number > len(habits):
            print("Invalid number.")
            return

        old_name = habits[number - 1]
        new_name = input("Enter new habit name: ").strip()

        if not new_name:
            print("Habit name cannot be empty.")
            return

        if new_name in habits and new_name != old_name:
            print("This habit already exists.")
            return

        habits[number - 1] = new_name

        if old_name in completed:
            completed[completed.index(old_name)] = new_name

        if old_name in streaks:
            streaks[new_name] = streaks.pop(old_name)

        for day in history:
           for day in history:
            if old_name in history[day]:
                history[day][history[day].index(old_name)] = new_name 

        save_data()
        print("Habit updated!")

    except ValueError:
        print("Please enter a valid number.")


def remove_habit():
    show_habits()

    if not habits:
        return

    try:
        number = int(input("\nEnter habit number to remove: "))

        if number < 1 or number > len(habits):
            print("Invalid number.")
            return

        habit = habits[number - 1]

        confirm = input(
            f"Are you sure you want to remove '{habit}'? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("Removal cancelled.")
            return

        habits.pop(number - 1)

        if habit in completed:
            completed.remove(habit)

        streaks.pop(habit, None)

        for day in history:
            if habit in history[day]:
                history[day].remove(habit)

        save_data()
        print("Habit removed!")

    except ValueError:
        print("Please enter a valid number.")


def search_habits():
    print("\n--- SEARCH HABITS ---")

    query = input("Enter habit name: ").strip().lower()

    if not query:
        print("Search cannot be empty.")
        return

    results = [
        habit for habit in habits
        if query in habit.lower()
    ]

    if results:
        print("\n--- SEARCH RESULTS ---")

        for number, habit in enumerate(results, start=1):
            status = "DONE" if habit in completed else "NOT DONE"
            print(f"{number}. {habit} - {status}")
    else:
        print("No habits found.")


while True:
    print("\n" + "=" * 30)
    print("       HABIT TRACKER")
    print("=" * 30)
    print(f"Date: {today}")

    print("\n1. Show habits")
    print("2. Mark habit completed")
    print("3. Statistics")
    print("4. Add habit")
    print("5. Remove habit")
    print("6. Calendar")
    print("7. Edit habit")
    print("8. Search habits")
    print("9. Exit")

    choice = input("\nChoose an option: ").strip()

    if choice == "1":
        show_habits()

    elif choice == "2":
        mark_completed()

    elif choice == "3":
        show_statistics()

    elif choice == "4":
        add_habit()

    elif choice == "5":
        remove_habit()

    elif choice == "6":
        show_calendar()

    elif choice == "7":
        edit_habit()

    elif choice == "8":
        search_habits()

    elif choice == "9":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")  