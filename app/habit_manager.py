import sqlite3
from datetime import datetime, timedelta
from app.habit import Habit

class HabitManager:
    def __init__(self):
        pass

    # Creates a new habit and saves it to the database.
    def create_habit(self, name, description, periodicity):
        creation_date = datetime.now().strftime("%Y-%m-%d")

        with sqlite3.connect('habits.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO habits (name, description, periodicity, creation_date)
                VALUES (?, ?, ?, ?)
            ''', (name, description, periodicity, creation_date))
            habit_id = cursor.lastrowid

        print(f"Habit '{name}' created successfully.")
        return Habit(habit_id, name, description, periodicity, creation_date)

    # Edit an existing habit in the database.
    def edit_habit(self, habit_name, new_name=None, new_description=None, new_periodicity=None):
        with sqlite3.connect('habits.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM habits WHERE name = ?", (habit_name,))
            result = cursor.fetchone()
            if not result:
                raise ValueError(f"Habit with name '{habit_name}' not found.")
            habit_id = result[0]

            if new_name:
                cursor.execute("UPDATE habits SET name = ? WHERE id = ?", (new_name, habit_id))
            if new_description:
                cursor.execute("UPDATE habits SET description = ? WHERE id = ?", (new_description, habit_id))
            if new_periodicity:
                cursor.execute("UPDATE habits SET periodicity = ? WHERE id = ?", (new_periodicity, habit_id))

        print(f"Habit '{habit_name}' updated successfully.")

    # Deletes a habit by name from the database.
    def delete_habit(self, habit_name):
        with sqlite3.connect('habits.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM habits WHERE name = ?", (habit_name,))
            if cursor.rowcount == 0:
                raise ValueError(f"Habit with name '{habit_name}' not found.")

        print(f"Habit '{habit_name}' deleted successfully.")

    # Returns all habits from the database.
    def list_habits(self):
        with sqlite3.connect('habits.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM habits")
            habits = cursor.fetchall()

        return [Habit.from_database(row) for row in habits]

    # Returns all habits with description and last completion date.
    def list_habits_with_details(self):
        conn = sqlite3.connect('habits.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT h.id, h.name, h.description, h.periodicity, 
                   COALESCE(MAX(c.completion_date), 'Never') AS last_completed
            FROM habits h
            LEFT JOIN completion c ON h.id = c.habit_id
            GROUP BY h.id, h.name, h.description, h.periodicity
            ORDER BY h.name
        ''')
        habits = cursor.fetchall()
        conn.close()

        return habits

    # Marks a habit as completed on a given date in the database.
    def mark_habit_completed(self, habit_id, completion_date):
        with sqlite3.connect('habits.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 1 FROM completion WHERE habit_id = ? AND completion_date = ?
            ''', (habit_id, completion_date))
            if cursor.fetchone():
                print(f"Habit with ID {habit_id} is already marked as completed on {completion_date}.")
                return

            cursor.execute('''
                INSERT INTO completion (habit_id, completion_date)
                VALUES (?, ?)
            ''', (habit_id, completion_date))

        # print(f"Habit with ID {habit_id} marked as completed on {completion_date}.")

    # Checks the status of all habits for a specific date with details.
    def check_habits_status(self, date):
        with sqlite3.connect('habits.db') as conn:
            cursor = conn.cursor()

            # Retrieve all habits with their periodicity and last completion date
            cursor.execute('''
                SELECT h.id, h.name, h.periodicity, 
                       COALESCE(MAX(c.completion_date), 'Never') AS last_completed
                FROM habits h
                LEFT JOIN completion c ON h.id = c.habit_id
                GROUP BY h.id, h.name, h.periodicity
            ''')
            habits = cursor.fetchall()

            completed = []
            pending = []

            current_date = datetime.strptime(date, "%Y-%m-%d")

            for habit_id, name, periodicity, last_completed in habits:
                if last_completed != 'Never':
                    last_completion_date = datetime.strptime(last_completed, "%Y-%m-%d")
                else:
                    last_completion_date = None

                # Check if the habit is completed or pending
                if periodicity == "daily":
                    if last_completion_date and last_completion_date.date() == current_date.date():
                        completed.append((name, periodicity, last_completed))
                    else:
                        pending.append((name, periodicity, last_completed))
                elif periodicity == "weekly":
                    # Check if the last completion is in the current week
                    current_week_start = current_date - timedelta(days=current_date.weekday())  # Start of the week
                    current_week_end = current_week_start + timedelta(days=6)  # End of the week

                    if last_completion_date and current_week_start.date() <= last_completion_date.date() <= current_week_end.date():
                        completed.append((name, periodicity, last_completed))
                    else:
                        pending.append((name, periodicity, last_completed))

        return completed, pending

    # Loads all completions of a habit from the database.
    def get_habit_completions(self, habit_id):
        with sqlite3.connect('habits.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT completion_date FROM completion
                WHERE habit_id = ?
                ORDER BY completion_date ASC
            ''', (habit_id,))
            completions = cursor.fetchall()

        return [completion[0] for completion in completions]

    # Returns the ID of a habit by its name.
    def get_habit_id_by_name(self, habit_name):
        with sqlite3.connect('habits.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM habits WHERE name = ?", (habit_name,))
            result = cursor.fetchone()

        if result:
            return result[0]
        else:
            raise ValueError(f"No habit found with name '{habit_name}'.")

    # Fetches all habits that are pending for the specified date, considering their periodicity.
    def get_pending_habits(self, date):
        with sqlite3.connect('habits.db') as conn:
            cursor = conn.cursor()

            # Retrieve all habits with their periodicity
            cursor.execute('''
                SELECT h.id, h.name, h.periodicity, 
                       (SELECT MAX(completion_date) 
                        FROM completion 
                        WHERE habit_id = h.id) AS last_completion
                FROM habits h
            ''')
            habits = cursor.fetchall()

            pending = []
            current_date = datetime.strptime(date, "%Y-%m-%d")

            for habit_id, name, periodicity, last_completion in habits:
                if last_completion:
                    last_completion_date = datetime.strptime(last_completion, "%Y-%m-%d")
                else:
                    last_completion_date = None

                # Determine if the habit is pending based on its periodicity
                if periodicity == "daily":
                    if not last_completion_date or last_completion_date.date() < current_date.date():
                        pending.append((habit_id, name, periodicity, last_completion))
                elif periodicity == "weekly":
                    # Check if the last completion is in the current week
                    current_week_start = current_date - timedelta(days=current_date.weekday())  # Start of the week
                    current_week_end = current_week_start + timedelta(days=6)  # End of the week

                    if not last_completion_date or not (
                            current_week_start.date() <= last_completion_date.date() <= current_week_end.date()):
                        pending.append((habit_id, name, periodicity, last_completion))

        return pending


