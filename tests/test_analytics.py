import unittest
import sqlite3
from app.analytics import longest_streak, filter_by_periodicity
from app.database import initialize_database, reset_database

class TestAnalytics(unittest.TestCase):
    @classmethod
    # Initialize the database before any tests are run.
    def setUpClass(cls):
        initialize_database()

    # Reset and reinitialize the database before each test.
    def setUp(self):
        reset_database()
        initialize_database()

        conn = sqlite3.connect('habits.db')
        cursor = conn.cursor()

        # Insert daily habit "Exercise"
        cursor.execute("INSERT INTO habits (name, description, periodicity, creation_date) VALUES (?, ?, ?, ?)",
                       ("Exercise", "Daily exercise", "daily", "2024-12-09"))
        cursor.execute("INSERT INTO completion (habit_id, completion_date) VALUES (?, ?)", (1, "2024-12-10"))
        cursor.execute("INSERT INTO completion (habit_id, completion_date) VALUES (?, ?)", (1, "2024-12-11"))

        # Insert weekly habit "Read"
        cursor.execute("INSERT INTO habits (name, description, periodicity, creation_date) VALUES (?, ?, ?, ?)",
                       ("Read", "Weekly reading", "weekly", "2024-12-09"))
        cursor.execute("INSERT INTO completion (habit_id, completion_date) VALUES (?, ?)", (2, "2024-12-09"))
        cursor.execute("INSERT INTO completion (habit_id, completion_date) VALUES (?, ?)", (2, "2024-12-16"))

        conn.commit()
        conn.close()

    # Test analytics for longest habit streak
    def test_longest_streak(self):
        streak = longest_streak()
        self.assertIn('daily', streak)
        self.assertIn('weekly', streak)

        # Check the daily streak
        self.assertEqual(streak['daily']['name'], 'Exercise')
        self.assertEqual(streak['daily']['streak'], 2)

        # Check the weekly streak
        self.assertEqual(streak['weekly']['name'], 'Read')
        self.assertEqual(streak['weekly']['streak'], 2)

    # Test analytics for habit filter
    def test_filter_by_periodicity(self):
        daily_habits = filter_by_periodicity("daily")
        weekly_habits = filter_by_periodicity("weekly")

        self.assertEqual(len(daily_habits), 1)
        self.assertEqual(daily_habits[0].name, "Exercise")
        self.assertEqual(len(weekly_habits), 1)
        self.assertEqual(weekly_habits[0].name, "Read")

if __name__ == "__main__":
    unittest.main()
