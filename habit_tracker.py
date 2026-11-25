import json
from datetime import date
from pathlib import Path

FILE = Path(__file__).parent / "habits.json"

def load_data():
    if FILE.exists():
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

data = load_data()

habits = data.get("habits", ["Study", "Python", "English", "Read", "Take a break"])
completed = data.get("completed", [])
last_date = data.get("last_date", "")
streaks = data.get("streaks", {})
history = data.get("history", {})
xp = data.get("xp", 0)

today = str(date.today())

if last_date != today:
    completed = []

def save_data():
    data = {
        "habits": habits,
        "completed": completed,
        "last_date": today,
        "streaks": streaks,
        "history": history,
        "xp": xp
    }
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_level():
    return xp // 100 + 1

def get_level_progress():
    return xp % 100

def show_profile():
    print("\n===== USER PROFILE =====")
    print(f"XP: {xp}")
    print(f"Level: {get_level()}")
    print(f"Progress: {get_level_progress()}/100 XP")
    print("=======================\n")

def show_habits():
    print("\n===== HABITS =====")
    if not habits:
        print("No habits yet.")
    for i, habit in enumerate(habits, 1):
        status = "[X]" if habit in completed else "[ ]"
        print(f"{i}. {status} {habit}")
    print("=================\n")

def mark_completed():
    show_habits()
    if not habits:
        return

    try:
        choice = int(input("Habit number: "))
        if choice < 1 or choice > len(habits):
            print("Invalid number.")
            return
    except ValueError:
        print("Enter a number.")
        return

    habit = habits[choice - 1]

    if habit in completed:
        print("Already completed today!")
        return

    global xp
    completed.append(habit)
    xp += 10

    if habit not in streaks:
        streaks[habit] = 0
    streaks[habit] += 1

    if today not in history:
        history[today] = []
    history[today].append(habit)

    print(f"\n{habit} completed! +10 XP")
    print(f"Your XP: {xp}")
    print(f"Your level: {get_level()}")

    save_data()

def show_calendar():
    print("\n===== HISTORY =====")
    if not history:
        print("No history yet.")
    for day in sorted(history):
        print(f"\n{day}:")
        for habit in history[day]:
            print(f"  - {habit}")
    print("==================\n")

def show_statistics():
    print("\n===== STATISTICS =====")
    print(f"Total habits: {len(habits)}")
    print(f"Completed today: {len(completed)}")
    print(f"Total XP: {xp}")
    print(f"Level: {get_level()}")

    print("\nStreaks:")
    for habit in habits:
        print(f"{habit}: {streaks.get(habit, 0)}")

    print("=====================\n")

def add_habit():
    habit = input("New habit: ").strip()
    if not habit:
        print("Habit name cannot be empty.")
        return
    if habit in habits:
        print("Habit already exists.")
        return

    habits.append(habit)
    streaks[habit] = 0
    save_data()
    print("Habit added!")

def edit_habit():
    show_habits()
    if not habits:
        return

    try:
        choice = int(input("Habit number to edit: "))
        if choice < 1 or choice > len(habits):
            print("Invalid number.")
            return
    except ValueError:
        print("Enter a number.")
        return

    old_name = habits[choice - 1]
    new_name = input("New name: ").strip()

    if not new_name:
        print("Name cannot be empty.")
        return
    if new_name in habits and new_name != old_name:
        print("Habit already exists.")
        return

    habits[choice - 1] = new_name
    for day in history:
     if old_name in streaks:
        streaks[new_name] = streaks.pop(old_name)
    else:
        streaks[new_name] = 0

    if old_name in completed:
        completed[completed.index(old_name)] = new_name

        for day in history:
           if old_name in history[day]:
             history[day][history[day].index(old_name)] = new_name

    save_data()
    print("Habit edited!")

def remove_habit():
    show_habits()
    if not habits:
        return

    try:
        choice = int(input("Habit number to remove: "))
        if choice < 1 or choice > len(habits):
            print("Invalid number.")
            return
    except ValueError:
        print("Enter a number.")
        return

    habit = habits.pop(choice - 1)

    if habit in completed:
        completed.remove(habit)

    streaks.pop(habit, None)

    for day in history:
        if habit in history[day]:
            history[day].remove(habit)

    save_data()
    print("Habit removed!")

def search_habits():
    query = input("Search: ").strip().lower()
    results = [h for h in habits if query in h.lower()]

    print("\n===== SEARCH =====")
    if results:
        for habit in results:
            status = "[X]" if habit in completed else "[ ]"
            print(f"{status} {habit}")
    else:
        print("No habits found.")
    print("=================\n")

def main():
    while True:
        print("===== HABIT TRACKER v1.6 =====")
        print("1. Show habits")
        print("2. Mark completed")
        print("3. Statistics")
        print("4. Add habit")
        print("5. Remove habit")
        print("6. Calendar / history")
        print("7. Edit habit")
        print("8. Search habits")
        print("9. User profile")
        print("10. Exit")
        print("==============================")

        choice = input("Choose: ")

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
            show_profile()
        elif choice == "10":
            save_data()
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

main()