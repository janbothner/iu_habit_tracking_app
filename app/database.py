import sqlite3
import os

DB_FILE = 'habits.db'

# Initializes the SQLite database with required tables.
def initialize_database():
    db_path = os.path.abspath(DB_FILE)
    # print(f"Initializing database at: {db_path}")

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Table: Habits
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                periodicity TEXT CHECK(periodicity IN ('daily', 'weekly')) NOT NULL,
                creation_date TEXT NOT NULL
            )
        ''')

        # Table: Completion
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS completion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completion_date TEXT NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
            )
        ''')

        conn.commit()
        # print("Database initialized successfully.")
    except sqlite3.Error as e:
        print(f"Error while initializing database: {e}")
    finally:
        conn.close()

# Resets the database by dropping and reinitializing tables.
def reset_database():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute('DROP TABLE IF EXISTS completion')
        cursor.execute('DROP TABLE IF EXISTS habits')

        conn.commit()
        # print("Database reset successfully.")
    except sqlite3.Error as e:
        print(f"Error while resetting database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    initialize_database()
