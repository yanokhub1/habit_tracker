import json
from datetime import date, timedelta
from pathlib import Path

FILE = Path(__file__).parent / "habits.json"

def load_data():
    if FILE.exists():
        try:
            with open(FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            print("Warning: data file could not be read.")
    return {}

data = load_data()

habits = data.get("habits", ["Study", "Python", "English", "Read", "Take a break"])
completed = data.get("completed", [])
last_date = data.get("last_date", "")
streaks = data.get("streaks", {})
best_streaks = data.get("best_streaks", {})
history = data.get("history", {})
xp = data.get("xp", 0)
achievements = data.get("achievements", [])

today = str(date.today())

if last_date != today:
    completed = []

def save_data():
    data = {
        "habits": habits,
        "completed": completed,
        "last_date": today,
        "streaks": streaks,
        "best_streaks": best_streaks,
        "history": history,
        "xp": xp,
        "achievements": achievements
    }

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_level():
    return xp // 100 + 1

def get_level_progress():
    return xp % 100

def calculate_streak(habit):
    days = sorted(
        day for day, items in history.items()
        if habit in items
    )

    streak = 0
    current_day = date.today()

    if str(current_day) in days:
        check_day = current_day
    else:
        check_day = current_day - timedelta(days=1)

    day_set = set(days)

    while str(check_day) in day_set:
        streak += 1
        check_day -= timedelta(days=1)

    return streak

def update_streaks():
    for habit in habits:
        streaks[habit] = calculate_streak(habit)
        best_streaks[habit] = max(
            best_streaks.get(habit, 0),
            streaks[habit]
        )

def check_achievements():
    total_completions = sum(len(items) for items in history.values())

    possible = {
        "First Step": total_completions >= 1,
        "Getting Started": xp >= 50,
        "Level Up": get_level() >= 2,
        "Dedicated": total_completions >= 5,
        "Habit Master": xp >= 500
    }

    for name, condition in possible.items():
        if condition and name not in achievements:
            achievements.append(name)
            print(f"\n🏆 ACHIEVEMENT UNLOCKED: {name}!")

def show_habits():
    update_streaks()

    print("\n===== HABITS =====")

    if not habits:
        print("No habits yet.")

    for i, habit in enumerate(habits, 1):
        status = "[X]" if habit in completed else "[ ]"
        streak = streaks.get(habit, 0)
        print(f"{i}. {status} {habit} 🔥 {streak} days")

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

    if today not in history:
        history[today] = []

    if habit not in history[today]:
        history[today].append(habit)

    update_streaks()
    check_achievements()

    print(f"\n{habit} completed! +10 XP")
    print(f"Your XP: {xp}")
    print(f"Your level: {get_level()}")
    print(f"🔥 Streak: {streaks[habit]} days")

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
    update_streaks()
    print("\n===== STATISTICS =====")
    print(f"Total habits: {len(habits)}")
    print(f"Completed today: {len(completed)}")
    print(f"Total XP: {xp}")
    print(f"Level: {get_level()}")

    print("\nStreaks:")

    for habit in habits:
        print(
            f"{habit}: {streaks.get(habit, 0)} days "
            f"(Best: {best_streaks.get(habit, 0)})"
        )

    print("=====================\n")

def show_profile():
    print("\n===== USER PROFILE =====")
    print(f"XP: {xp}")
    print(f"Level: {get_level()}")
    print(f"Progress: {get_level_progress()}/100 XP")
    print(f"Achievements: {len(achievements)}")
    print("=======================\n")

def show_achievements():
    print("\n===== ACHIEVEMENTS =====")

    achievement_list = {
        "First Step": "Complete your first habit",
        "Getting Started": "Earn 50 XP",
        "Level Up": "Reach Level 2",
        "Dedicated": "Complete 5 habits",
        "Habit Master": "Earn 500 XP"
    }

    for name, description in achievement_list.items():
        if name in achievements:
            print(f"🏆 {name} - UNLOCKED")
        else:
            print(f"🔒 {name} - {description}")

    print("=======================\n")

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
    best_streaks[habit] = 0

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

    if old_name in streaks:
        streaks[new_name] = streaks.pop(old_name)
    else:
        streaks[new_name] = 0

    if old_name in best_streaks:
        best_streaks[new_name] = best_streaks.pop(old_name)
    else:
        best_streaks[new_name] = 0

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
    best_streaks.pop(habit, None)

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
            print(f"{status} {habit} 🔥 {streaks.get(habit, 0)} days")
    else:
        print("No habits found.")

    print("=================\n")

def main():
    update_streaks()
    check_achievements()
    save_data()

    while True:
        print("===== HABIT TRACKER v1.7 =====")
        print("1. Show habits")
        print("2. Mark completed")
        print("3. Statistics")
        print("4. Add habit")
        print("5. Remove habit")
        print("6. Calendar / history")
        print("7. Edit habit")
        print("8. Search habits")
        print("9. User profile")
        print("10. Achievements")
        print("11. Exit")
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
            show_achievements()
        elif choice == "11":
            save_data()
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

main()