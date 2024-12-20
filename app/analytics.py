import sqlite3
from app.habit import Habit

# Calculates the longest streak for both daily and weekly habits from the database.
# Returns the longest streaks with their habit names.
def longest_streak():
    with sqlite3.connect('habits.db') as conn:
        cursor = conn.cursor()

        # Query for the longest daily streak
        cursor.execute('''
            SELECT h.name, MAX(streak) AS longest_streak
            FROM (
                SELECT habit_id, COUNT(*) AS streak
                FROM (
                    SELECT habit_id, completion_date,
                           ROW_NUMBER() OVER (PARTITION BY habit_id ORDER BY completion_date) -
                           CAST(strftime('%s', completion_date) / 86400 AS INTEGER) AS group_id
                    FROM completion
                    JOIN habits h ON completion.habit_id = h.id
                    WHERE h.periodicity = 'daily'
                )
                GROUP BY habit_id, group_id
            ) streaks
            JOIN habits h ON streaks.habit_id = h.id
        ''')
        daily_result = cursor.fetchone()

        # Query for the longest weekly streak
        cursor.execute('''
            SELECT h.name, MAX(streak) AS longest_streak
            FROM (
                SELECT habit_id, COUNT(*) AS streak
                FROM (
                    SELECT habit_id, completion_date,
                           ROW_NUMBER() OVER (PARTITION BY habit_id ORDER BY completion_date) -
                           CAST(strftime('%s', completion_date) / 604800 AS INTEGER) AS group_id
                    FROM completion
                    JOIN habits h ON completion.habit_id = h.id
                    WHERE h.periodicity = 'weekly'
                )
                GROUP BY habit_id, group_id
            ) streaks
            JOIN habits h ON streaks.habit_id = h.id
        ''')
        weekly_result = cursor.fetchone()

    # Extract results
    daily_name, daily_streak = daily_result if daily_result and daily_result[0] else ("None", 0)
    weekly_name, weekly_streak = weekly_result if weekly_result and weekly_result[0] else ("None", 0)

    return {
        "daily": {"name": daily_name, "streak": daily_streak},
        "weekly": {"name": weekly_name, "streak": weekly_streak},
    }

# Filters habits based on their periodicity (daily or weekly) from the database.
# Returns a list of Habit objects matching the periodicity.
def filter_by_periodicity(periodicity):
    with sqlite3.connect('habits.db') as conn:
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, name, description, periodicity, creation_date
            FROM habits
            WHERE periodicity = ?
        ''', (periodicity,))
        habits = cursor.fetchall()

    return [Habit.from_database(row) for row in habits]