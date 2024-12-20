import unittest
import sqlite3
from app.habit_manager import HabitManager
from app.database import initialize_database, reset_database

class TestHabitManager(unittest.TestCase):
    @classmethod
    # Initialize the database before any tests are run.
    def setUpClass(cls):
        initialize_database()

    # Reset the database before each test.
    def setUp(self):
        reset_database()
        initialize_database()
        self.manager = HabitManager()

    # Create a test habit in database table
    def test_create_habit(self):
        habit = self.manager.create_habit("Exercise", "Daily exercise", "daily")
        conn = sqlite3.connect('habits.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM habits WHERE name = 'Exercise'")
        result = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Exercise")

    # Test to edit a habit in database table
    def test_edit_habit(self):
        self.manager.create_habit("Exercise", "Daily exercise", "daily")
        self.manager.edit_habit("Exercise", new_name="Morning Run", new_description="Run in the morning", new_periodicity="weekly")

        conn = sqlite3.connect('habits.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, description, periodicity FROM habits WHERE name = 'Morning Run'")
        result = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Morning Run")
        self.assertEqual(result[1], "Run in the morning")
        self.assertEqual(result[2], "weekly")

    # Test to delete a habit in database
    def test_delete_habit(self):
        self.manager.create_habit("Exercise", "Daily exercise", "daily")
        self.manager.delete_habit("Exercise")

        conn = sqlite3.connect('habits.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM habits WHERE name = 'Exercise'")
        result = cursor.fetchone()
        conn.close()

        self.assertIsNone(result)

    # Test to create habits and then list them
    def test_list_habits(self):
        self.manager.create_habit("Exercise", "Daily exercise", "daily")
        self.manager.create_habit("Read", "Weekly reading", "weekly")
        habits = self.manager.list_habits()
        self.assertEqual(len(habits), 2)

    # Test to create and then mark a habit as completed
    def test_mark_habit_completed(self):
        habit = self.manager.create_habit("Exercise", "Daily exercise", "daily")
        self.manager.mark_habit_completed(habit.id, "2024-12-10")

        conn = sqlite3.connect('habits.db')
        cursor = conn.cursor()
        cursor.execute("SELECT completion_date FROM completion WHERE habit_id = ?", (habit.id,))
        result = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], "2024-12-10")

if __name__ == "__main__":
    unittest.main()
    