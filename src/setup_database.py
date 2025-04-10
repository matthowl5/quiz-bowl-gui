import sqlite3

# Define your course categories
COURSES = [
    "computer_applications",
    "business_law",
    "managerial_finance",
    "database_management",
    "business_analytics"
]

def create_tables():
    conn = sqlite3.connect("quiz_bowl.db")
    cursor = conn.cursor()

    for course in COURSES:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {course} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                correct_answer TEXT NOT NULL
            );
        """)

    conn.commit()
    conn.close()
    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()
