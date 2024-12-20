from datetime import datetime, timedelta
import sqlite3

class Habit:
    def __init__(self, id, name, description, periodicity, creation_date):
        self.id = id
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.creation_date = creation_date

    @staticmethod
    # Creates a Habit instance from a database row.
    def from_database(row):
        return Habit(row[0], row[1], row[2], row[3], row[4])

    @staticmethod
    # Fetches all completion dates for the habit from the database.
    def get_completion_dates(habit_id):
        conn = sqlite3.connect('habits.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT completion_date 
            FROM completion 
            WHERE habit_id = ? 
            ORDER BY completion_date ASC
        ''', (habit_id,))
        completion_dates = [row[0] for row in cursor.fetchall()]
        conn.close()
        return completion_dates

    @staticmethod
    # Marks a habit as completed on a given date.
    def mark_completed(habit_id, completion_date):
        conn = sqlite3.connect('habits.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO completion (habit_id, completion_date)
            VALUES (?, ?)
        ''', (habit_id, completion_date))
        conn.commit()
        conn.close()

    @staticmethod
    # Calculates the longest streak based on completion data.
    def calculate_streak(completion_dates):
        if not completion_dates:
            return 0

        streak = 1
        longest_streak = 1

        # Convert dates to datetime objects
        completion_dates = [datetime.strptime(date, "%Y-%m-%d") for date in completion_dates]
        completion_dates.sort()

        for i in range(1, len(completion_dates)):
            if completion_dates[i] - completion_dates[i - 1] == timedelta(days=1):
                streak += 1
                longest_streak = max(longest_streak, streak)
            else:
                streak = 1

        return longest_streak

    # Calculates the longest streak for this habit using the database.
    def get_longest_streak(self):
        completion_dates = self.get_completion_dates(self.id)
        return self.calculate_streak(completion_dates)

    # Calculates the current streak for this habit.
    def get_current_streak(self):
        completion_dates = self.get_completion_dates(self.id)
        if not completion_dates:
            return 0

        # Convert dates to datetime objects
        completion_dates = [datetime.strptime(date, "%Y-%m-%d") for date in completion_dates]
        completion_dates.sort()

        streak = 1
        today = datetime.now().date()

        for i in range(len(completion_dates) - 1, 0, -1):
            if (today - completion_dates[i].date()).days > 1:
                break
            streak += 1

        return streak
