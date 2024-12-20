from app.database import initialize_database
from app.cli import display_menu

if __name__ == "__main__":
    # Initializing the Database
    initialize_database()

    # Start CLI
    display_menu()
