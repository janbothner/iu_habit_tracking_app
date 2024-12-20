from app.habit_manager import HabitManager
from app.analytics import longest_streak, filter_by_periodicity
from database_seeder.seeder import seed_database
from app.database import reset_database, initialize_database

# Displays the main menu of the Habit Tracking App
def display_menu():
    manager = HabitManager()

    while True:
        print("\nHabit Tracking App")
        print("1. Create a habit")
        print("2. View Habits")
        print("3. Edit Habit")
        print("4. Delete Habit")
        print("5. Mark Habit as Completed")
        print("6. Check Habit Status")
        print("7. Analysis of Habits")
        print("8. Seed Database with Test Data")
        print("9. Rebuild Database")
        print("10. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Name of Habit: ")
            description = input("Description: ")
            periodicity = input("Periodicity (daily/weekly): ")
            manager.create_habit(name, description, periodicity)
            print(f"Habit '{name}' created successfully.")
        elif choice == "2":
            habits = manager.list_habits_with_details()
            if habits:
                for habit in habits:
                    habit_id, name, description, periodicity, last_completed = habit
                    print(f"- {name} ({periodicity})")
                    print(f"  Description: {description}")
                    print(f"  Last Completed: {last_completed}")
            else:
                print("No habits found.")
        elif choice == "3":
            habit_name = input("Name of the Habit to Edit: ")
            new_name = input("New name (leave blank if it shouldn´t be updated): ") or None
            new_description = input("New Description (leave blank if it shouldn´t be updated): ") or None
            new_periodicity = input(
                "New Periodicity (daily/weekly, leave blank if it shouldn´t be updated): ") or None
            try:
                manager.edit_habit(habit_name, new_name, new_description, new_periodicity)
                print(f"Habit '{habit_name}' was successfully updated.")
            except ValueError as e:
                print(e)
        elif choice == "4":
            habit_name = input("Name of the habit to delete: ")
            manager.delete_habit(habit_name)
            print(f"Habit '{habit_name}' was deleted successfully.")
        elif choice == "5":
            mark_habit_as_completed(manager)
        elif choice == "6":
            check_habit_status(manager)
        elif choice == "7":
            analytics_menu()
        elif choice == "8":
            seed_database()
        elif choice == "9":
            rebuild_database()
        elif choice == "10":
            break
        else:
            print("Invalid Option.")

# Rebuilds the database: Drops all tables and recreates them
def rebuild_database():
    confirm = input("Are you sure you want to rebuild the database? All data will be lost! (yes/no): ")
    if confirm.lower() == "yes":
        reset_database()
        initialize_database()
        print("Database has been rebuilt successfully.")
    else:
        print("Database rebuild canceled.")

# Shows all pending habits with additional details and allows the user to mark one as completed.
def mark_habit_as_completed(manager):
    date = input("Enter the date of completion (YYYY-MM-DD): ")
    pending = manager.get_pending_habits(date)

    if pending:
        print("\nPending Habits:")
        for idx, (habit_id, name, periodicity, last_completion) in enumerate(pending, start=1):
            last_completion_display = last_completion if last_completion else "Never"
            print(f"{idx}. {name} ({periodicity}, Last Completed: {last_completion_display})")

        choice = int(input("Select the number of the habit to mark as completed: "))
        if 1 <= choice <= len(pending):
            habit_id = pending[choice - 1][0]  # Get the habit ID
            manager.mark_habit_completed(habit_id, date)
            print(f"Habit '{pending[choice - 1][1]}' marked as completed on {date}.")
        else:
            print("Invalid choice.")
    else:
        print("No pending habits for the selected date.")

# Displays all habits categorized into completed and pending with details.
def check_habit_status(manager):
    date = input("Enter the date to check (YYYY-MM-DD): ")
    completed, pending = manager.check_habits_status(date)

    print("\nCompleted Habits:")
    if completed:
        for name, periodicity, last_completed in completed:
            print(f"- {name} ({periodicity} / Last Completed: {last_completed})")
    else:
        print("No completed habits.")

    print("\nPending Habits:")
    if pending:
        for name, periodicity, last_completed in pending:
            print(f"- {name} ({periodicity} / Last Completed: {last_completed})")
    else:
        print("No pending habits.")

# Displays analysis options for habits.
def analytics_menu():
    while True:
        print("\nAnalysis of Habits")
        print("1. View Longest Streak")
        print("2. Filter habits by periodicity")
        print("3. Back to main menu")
        choice = input("Choose an option: ")

        if choice == "1":
            try:
                streaks = longest_streak()
                print(f"The longest daily streak is: {streaks['daily']['streak']} days on habit: {streaks['daily']['name']}.")
                print(f"The longest weekly streak is: {streaks['weekly']['streak']} weeks on habit: {streaks['weekly']['name']}.")
            except ValueError:
                print("No habits found.")
        elif choice == "2":
            periodicity = input("Select Periodicity (daily/weekly): ")
            filtered_habits = filter_by_periodicity(periodicity)
            if filtered_habits:
                print(f"\nHabits with periodicity '{periodicity}':")
                for habit in filtered_habits:
                    print(f"- {habit.name}: {habit.description}")
            else:
                print(f"No habits with periodicity '{periodicity}' found.")
        elif choice == "3":
            break
        else:
            print("Invalid Option.")
