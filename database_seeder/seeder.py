import sqlite3
from datetime import datetime, timedelta
import random

DB_FILE = 'habits.db'

# Seeds the database with test data.
def seed_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 5 Daily Habits
    daily_habits = [
        ("Drink Water", "Drink 8 glasses of water", "daily"),
        ("Exercise", "30 minutes of physical exercise", "daily"),
        ("Read", "Read 20 pages of a book", "daily"),
        ("Meditate", "10 minutes of meditation", "daily"),
        ("Journal", "Write down thoughts and goals", "daily"),
    ]

    # 5 Weekly Habits
    weekly_habits = [
        ("Grocery Shopping", "Buy weekly groceries", "weekly"),
        ("Clean House", "Deep clean the house", "weekly"),
        ("Meal Prep", "Prepare meals for the week", "weekly"),
        ("Call Family", "Call parents or siblings", "weekly"),
        ("Review Goals", "Review weekly goals and progress", "weekly"),
    ]

    # Function to check if a habit exists
    def habit_exists(name):
        cursor.execute("SELECT 1 FROM habits WHERE name = ?", (name,))
        return cursor.fetchone() is not None

    # Insert Daily Habits
    for habit in daily_habits:
        if not habit_exists(habit[0]):
            cursor.execute('''
                INSERT INTO habits (name, description, periodicity, creation_date)
                VALUES (?, ?, ?, ?)
            ''', (*habit, datetime.now().strftime("%Y-%m-%d")))

    # Insert Weekly Habits
    for habit in weekly_habits:
        if not habit_exists(habit[0]):
            cursor.execute('''
                INSERT INTO habits (name, description, periodicity, creation_date)
                VALUES (?, ?, ?, ?)
            ''', (*habit, datetime.now().strftime("%Y-%m-%d")))

    conn.commit()

    # Fetch all habit IDs
    cursor.execute("SELECT id, periodicity FROM habits")
    habits = cursor.fetchall()

    # Generate completion dates for the last 4 weeks
    today = datetime.now()
    for habit_id, periodicity in habits:
        if periodicity == "daily":
            # Ensure there is at least one completion per day for the last 4 weeks
            for days_ago in range(28):  # 4 weeks = 28 days
                completion_date = today - timedelta(days=days_ago)
                cursor.execute('''
                    INSERT OR IGNORE INTO completion (habit_id, completion_date)
                    VALUES (?, ?)
                ''', (habit_id, completion_date.strftime("%Y-%m-%d")))
        elif periodicity == "weekly":
            # Ensure there is at least one completion per week for the last 4 weeks
            for weeks_ago in range(4):  # 4 weeks
                completion_date = today - timedelta(weeks=weeks_ago)
                cursor.execute('''
                    INSERT OR IGNORE INTO completion (habit_id, completion_date)
                    VALUES (?, ?)
                ''', (habit_id, completion_date.strftime("%Y-%m-%d")))

    # Add some random completions for diversity
    for habit_id, _ in habits:
        num_completions = random.randint(5, 10)  # Random number of completions
        for _ in range(num_completions):
            random_date = today - timedelta(days=random.randint(1, 28))
            cursor.execute('''
                INSERT OR IGNORE INTO completion (habit_id, completion_date)
                VALUES (?, ?)
            ''', (habit_id, random_date.strftime("%Y-%m-%d")))

    conn.commit()
    conn.close()

    print("Database seeded successfully with test data.")

if __name__ == "__main__":
    seed_database()
