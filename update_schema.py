import sqlite3

def update_schema():
    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect('workout_database.db')

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Execute SQL commands
    cursor.execute("ALTER TABLE workout ADD COLUMN date DATE NOT NULL;")

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

if __name__ == "__main__":
    update_schema()
