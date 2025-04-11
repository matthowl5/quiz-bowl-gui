# Quiz Bowl GUI

A Python-based GUI application for conducting quiz bowl-style quizzes across five business-related courses. Built using `tkinter`, the app includes both a quiz-taker interface and an admin interface for managing questions.

IMPORTANT: The final version of the code is contained in the file main.py. The older code, which was worked on over time, can be viewed in quiz_gui.py.
The file setup_database.py was used early in the project to create the database.
The file add_question.py was used early in the project to test the database by manually adding questions.

---

## 🧠 Courses Covered

- Computer Applications  
- Business Law  
- Managerial Finance  
- Database Management  
- Business Analytics  

---

## 🔐 Admin Access Passcode

The password for admin login is: jimmyjenkins

> 📁 This is included here per project requirements so the instructor can easily access it.

---

## 🚀 How to Run the App

### 📦 Requirements

Ensure you have Python 3 installed. This app uses only built-in libraries (`tkinter`, `sqlite3`), so no additional packages are required.

### ▶️ Launching the App

1. **Clone or download** the repository:
   ```bash
   git clone https://github.com/your-username/quiz-bowl-gui.git
   cd quiz-bowl-gui
2. Run the app using Python:
    ```bash
    python main.py

🧩 App Features
For Quiz-Takers:
    Select one of five courses to start a quiz.

    Answer multiple-choice questions (A/B/C/D).

    Get immediate feedback and a final score summary.

For Admins:
    Access a secure admin panel using the passcode.

    Add new questions to any course.

    View existing questions, with delete capability.

    Edit existing questions.

    Questions are stored in a persistent local SQLite database.

