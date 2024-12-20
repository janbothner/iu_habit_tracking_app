import sqlite3
import unittest
from unittest.mock import patch
from app.cli import display_menu
from app.database import initialize_database, reset_database

class TestCLI(unittest.TestCase):
    @classmethod
    # Initialize the database before any tests are run.
    def setUpClass(cls):
        initialize_database()

    # Reset the database before each test.
    def setUp(self):
        reset_database()
        initialize_database()

    # Test to create and list a habit
    @patch("builtins.input", side_effect=[
        "1", "Meditation", "Morning meditation", "daily",  # Create habit
        "2",  # View habits
        "10"  # Exit
    ])
    @patch("builtins.print")
    def test_create_and_list_habits(self, mock_print, mock_input):
        display_menu()

        conn = sqlite3.connect('habits.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM habits WHERE name = 'Meditation'")
        result = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Meditation")

    # Test to seed database with sample data
    @patch("builtins.input", side_effect=[
        "8",  # Seed Database
        "2",  # View Habits
        "10"  # Exit
    ])
    @patch("builtins.print")
    def test_seed_database(self, mock_print, mock_input):
        display_menu()

        conn = sqlite3.connect('habits.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM habits")
        result = cursor.fetchone()
        conn.close()

        self.assertGreaterEqual(result[0], 10)

    # Test to rebuild database
    @patch("builtins.input", side_effect=[
        "9",  # Rebuild Database
        "2",  # View Habits
        "10"  # Exit
    ])
    @patch("builtins.print")
    def test_rebuild_database(self, mock_print, mock_input):
        display_menu()

        conn = sqlite3.connect('habits.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM habits")
        result = cursor.fetchone()
        conn.close()

        self.assertEqual(result[0], 0)

    # Test to create, mark a habit as completed and check habit status
    @patch("builtins.input", side_effect=[
        "1", "Exercise", "Daily exercise", "daily",  # Create habit
        "5", "2024-12-14", "1",  # Mark habit as completed
        "6", "2024-12-14",  # Check habit status
        "10"  # Exit
    ])
    @patch("builtins.print")
    def test_mark_and_check_habit_status(self, mock_print, mock_input):
        display_menu()

        # Verify that the habit completion has been saved correctly
        conn = sqlite3.connect('habits.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM completion WHERE completion_date = '2024-12-14'")
        result = cursor.fetchone()
        conn.close()

        # Debugging-Log
        # print(f"Database completion count: {result[0]}")

        # Verify that habit has been saved
        self.assertEqual(result[0], 1)

    # Test to get the longest streak for a weekly habit
    @patch("builtins.input", side_effect=[
        "1", "Read", "Weekly reading", "weekly",  # Create weekly habit
        "7", "1",  # Analysis of Habits -> Longest streak
        "3",  # Back to main menu
        "10"  # Exit
    ])
    @patch("builtins.print")
    def test_analysis_longest_streak(self, mock_print, mock_input):
        display_menu()

        output = "\n".join(call.args[0] for call in mock_print.call_args_list if call.args)
        self.assertIn("The longest daily streak is", output)
        self.assertIn("The longest weekly streak is", output)

if __name__ == "__main__":
    unittest.main()
