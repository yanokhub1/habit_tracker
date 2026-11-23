import json

def load_data():
    with open("habits.json", "r") as file:
        data = json.load(file)
    return data["habits"], data["completed"]

def save_data():
    data = {
        "habits": habits,
        "completed": completed
    }
    with open("habits.json", "w") as file:
        json.dump(data, file, indent=4)

habits, completed = load_data()

print("=" * 30)
print("       HABIT TRACKER")
print("=" * 30)

while True:
    print("\n1. Show habits")
    print("2. Mark habit as completed")
    print("3. Show statistics")
    print("4. Add a new habit")
    print("5. Remove a habit")
    print("6. Exit")

    choice = input("\nChoose an option: ")

    if choice == "1":
        print("\nYour habits:")
        for i, habit in enumerate(habits, start=1):
            status = "DONE" if habit in completed else "NOT DONE"
            print(f"{i}. {habit} — {status}")

    elif choice == "2":
        print("\nChoose a habit:")
        for i, habit in enumerate(habits, start=1):
            print(f"{i}. {habit}")

        number = input("Enter habit number: ")

        if number.isdigit():
            number = int(number)

            if 1 <= number <= len(habits):
                habit = habits[number - 1]

                if habit not in completed:
                    completed.append(habit)
                    save_data()
                    print(f"{habit} completed!")
                else:
                    print("This habit is already completed.")
            else:
                print("Invalid habit number.")
        else:
            print("Please enter a number.")

    elif choice == "3":
        total = len(habits)
        done = len(completed)

        print("\nToday's statistics:")
        print(f"Completed: {done}/{total}")
        print(f"Remaining: {total - done}")

        if total > 0:
            percentage = done / total * 100
            print(f"Progress: {percentage:.0f}%")

    elif choice == "4":
        new_habit = input("Enter a new habit: ")

        if new_habit.strip():
            habits.append(new_habit.strip())
            save_data()
            print(f"Habit '{new_habit}' added!")
        else:
            print("Habit name cannot be empty.")

    elif choice == "5":
        print("\nYour habits:")
        for i, habit in enumerate(habits, start=1):
            print(f"{i}. {habit}")

        number = input("Enter habit number to remove: ")

        if number.isdigit():
            number = int(number)

            if 1 <= number <= len(habits):
                removed_habit = habits.pop(number - 1)

                if removed_habit in completed:
                    completed.remove(removed_habit)

                save_data()
                print(f"Habit '{removed_habit}' removed!")
            else:
                print("Invalid habit number.")
        else:
            print("Please enter a number.")

    elif choice == "6":
        print("Goodbye! Keep going!")
        break

    else:
        print("Invalid option. Try again.")