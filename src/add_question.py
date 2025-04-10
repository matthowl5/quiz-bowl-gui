import sqlite3

COURSES = [
    "computer_applications",
    "business_law",
    "managerial_finance",
    "database_management",
    "business_analytics"
]

def add_question():
    print("Choose a course to add a question to:")
    for i, course in enumerate(COURSES, start=1):
        print(f"{i}. {course}")

    choice = int(input("Enter the number: "))
    if not (1 <= choice <= len(COURSES)):
        print("Invalid choice.")
        return

    course = COURSES[choice - 1]

    question = input("Enter the question: ")
    option_a = input("Option A: ")
    option_b = input("Option B: ")
    option_c = input("Option C: ")
    option_d = input("Option D: ")

    correct_answer = input("Enter correct option (A, B, C, or D): ").upper()
    if correct_answer not in ['A', 'B', 'C', 'D']:
        print("Invalid answer. Must be A, B, C, or D.")
        return

    conn = sqlite3.connect("quiz_bowl.db")
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO {course} (question, option_a, option_b, option_c, option_d, correct_answer)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (question, option_a, option_b, option_c, option_d, correct_answer))

    conn.commit()
    conn.close()
    print("Question added successfully.")

if __name__ == "__main__":
    add_question()
