# Python Habit Tracking App
This Habit Tracking App is a command-line application designed to help users create, manage and analyze their daily and weekly habits. It offers features like habit streak tracking, database management and detailed analytics, all within a simple and intuitive interface.

## Features
- Create, view, edit and delete daily or weekly habits.
- Track habit completion and calculate streaks for analysis.
- Seed the database with sample data for testing.
- Reset and rebuild the database.
- Comprehensive unit tests to ensure reliability.

## Install Required Dependencies
Before running the application, install the required Python libraries:
```
pip install -r requirements.txt
```

## Run Habit Tracking App
1. Open your terminal.
2. Switch to the app folder:
```
cd c:\PATHTOFOLDER
```
3. Now run the Habit Tracking App:
```
python main.py
```

---

## Database
The application uses an SQLite database file (`habits.db`) to store habits and their completions. If the database doesn't exist, it will be created automatically when the application is first run.

### Run Database Seeder
1. Run the Habit Tracking App.
2. In the main menu choose point 8. to run database seeder.
3. Confirm your insert with "enter" and the database seeder will start to create sample data inside the database.
4. You can see the sample data by viewing all habits or checking the habit status.

---

## Unittest Habit Tracking App
The application includes unit tests to validate core functionality:
- `test_analytics.py` ensures analytics like streak calculation are accurate.
- `test_cli.py` verifies CLI interactions and data integration.
- `test_habit_manager.py` validates habit management operations, such as creating, editing, and deleting habits.

### Run Unittest Habit Tracking App
1. Open your terminal.
2. Switch to the app folder:
```
cd c:\PATHTOFOLDER
```
3. The following code will run all unittests for the Habit Tracking App:
```
python -m unittest discover tests/
```
4. You will see an "OK" if the unittests passing without any errors. If there are any errors detected you will get an alert in the CLI.

---

## File & Folder structure of the Habit Tracking App
- Folders:
  - app = Contains all the core Python files for the app's functionality, such as managing habits, CLI operations, and analytics.
  - database_seeder = Includes the script to seed the database with sample data for testing or demonstration purposes.
  - tests = Stores all the unittest files to validate the functionality of the app.
- Files:
  - analytics.py = Contains functions for analyzing habits, such as calculating streaks and filtering habits by periodicity.
  - cli.py = Implements the command-line interface (CLI) to interact with the Habit Tracking App, providing options for managing habits and analyzing data.
  - database.py = Manages the initialization and reset operations for the SQLite database, including the creation of necessary tables. 
  - habit.py = Defines the Habit class, representing the core attributes and behaviors of a habit.
  - habit_manager.py = Contains the HabitManager class, which handles operations such as creating, editing, deleting, and tracking habits in the database.
  - seeder.py = Script for seeding the database with sample daily and weekly habits, along with random completion data for demonstration or testing.
  - test_analytics.py = Includes test cases for the analytics functions, such as longest streak calculation and filtering by periodicity.
  - test_cli = Contains test cases for the CLI, ensuring correct user interaction and integration with the app’s functions.
  - test_habit_manager.py = Tests the HabitManager functionality, such as habit creation, deletion, and marking completion.
  - habits.db = The SQLite database file that stores all the habits and their completion data.
  - main.py = The entry point of the application that initializes the database and launches the CLI.
  - README.md = Provides an overview of the project, including its purpose, features, installation steps, and usage instructions.
  - requirements.txt = Lists all the required Python libraries and dependencies needed to run the application.

---
