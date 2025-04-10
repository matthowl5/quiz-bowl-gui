import tkinter as tk
from tkinter import messagebox
import sqlite3
import random

# Constants for Database and Design
DB_FILE = "quiz_bowl.db"
COURSES = [
    "Computer Applications",
    "Business Law",
    "Managerial Finance",
    "Database Management",
    "Business Analytics"
]
COLORS = {
    "bg": "#ffedd8",           # Warm pastel yellow (background)
    "accent": "#ff6f61",       # Vibrant coral orange (accent color)
    "button": "#59cd90",       # Bright mint green (buttons)
    "button_hover": "#52b788", # Deeper mint for hover effect
    "text": "#23395d",         # Rich navy blue (text)
    "highlight": "#84a59d",    # Soft sage green (highlighted selections)
}
FONTS = {
    "header": ("Comic Sans MS", 24, "bold"),  # Playful and fun
    "body": ("Tahoma", 14),                  # Clean and easy-to-read
    "button": ("Verdana", 12, "bold"),       # Modern and crisp
}

class QuizApp:
    """A cheerful GUI app for the Quiz Bowl."""

    def __init__(self, master):
        """Initialize the main window."""
        self.master = master
        self.master.title("Quiz Bowl")
        self.master.configure(bg=COLORS["bg"])
        self.course = None
        self.questions = []
        self.current_question = 0
        self.score = 0
        self.show_course_selection()

    def show_course_selection(self):
        """Display the course selection screen."""
        self.clear_window()

        tk.Label(self.master, text="🌟 Quiz Bowl 🌟", font=FONTS["header"],
                 fg=COLORS["text"], bg=COLORS["bg"]).pack(pady=20)

        tk.Label(self.master, text="Choose a course category:", font=FONTS["body"],
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=10)

        for course in COURSES:
            tk.Button(
                self.master,
                text=course,
                command=lambda c=course: self.start_quiz(c),
                bg=COLORS["button"], fg="white", activebackground=COLORS["button_hover"],
                relief="flat", bd=2, padx=10, pady=5, font=FONTS["button"]
            ).pack(pady=6, ipadx=10)

    def start_quiz(self, course):
        """Initialize the quiz for the selected course."""
        self.course = course
        self.questions = self.get_questions(course)
        if not self.questions:
            messagebox.showinfo("No Questions", "This category has no questions yet.")
            return
        self.current_question = 0
        self.score = 0
        self.show_question()

    def get_questions(self, course):
        """Retrieve and shuffle questions for the selected course."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {course.replace(' ', '_').lower()}")
        rows = cursor.fetchall()
        conn.close()
        random.shuffle(rows)
        return rows

    def show_question(self):
        """Display the current question and answer options."""
        self.clear_window()

        if self.current_question >= len(self.questions):
            self.show_score()
            return

        q = self.questions[self.current_question]
        question_text = q[1]
        options = q[2:6]
        self.correct_answer = q[6]

        tk.Label(
            self.master,
            text=f"Q{self.current_question + 1}: {question_text}",
            wraplength=450, font=FONTS["body"], bg=COLORS["bg"],
            fg=COLORS["text"], justify="left"
        ).pack(pady=20)

        self.selected = tk.StringVar()
        for label, option in zip(["A", "B", "C", "D"], options):
            tk.Radiobutton(
                self.master,
                text=f"{label}. {option}",
                variable=self.selected,
                value=label,
                font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"],
                selectcolor=COLORS["highlight"], activebackground=COLORS["bg"],
                anchor="w", padx=20
            ).pack(fill="x", padx=30, pady=4)

        tk.Button(
            self.master, text="Submit", command=self.check_answer,
            bg=COLORS["accent"], fg="white", font=FONTS["button"],
            padx=10, pady=6, relief="flat"
        ).pack(pady=25)

    def check_answer(self):
        """Check the selected answer and proceed to the next question."""
        selected = self.selected.get()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an answer.")
            return
        if selected == self.correct_answer:
            self.score += 1
        self.current_question += 1
        self.show_question()

    def show_score(self):
        """Display the final score."""
        self.clear_window()

        tk.Label(
            self.master,
            text=f"🎉 Your Score: {self.score} / {len(self.questions)}",
            font=FONTS["header"], fg=COLORS["text"], bg=COLORS["bg"]
        ).pack(pady=40)

        tk.Button(
            self.master, text="Take Another Quiz", command=self.show_course_selection,
            bg=COLORS["button"], fg="white", font=FONTS["button"], padx=10, pady=5
        ).pack(pady=10)

        tk.Button(
            self.master, text="Quit", command=self.master.quit,
            bg=COLORS["accent"], fg="white", font=FONTS["button"], padx=10, pady=5
        ).pack(pady=10)

    def clear_window(self):
        """Remove all widgets from the window."""
        for widget in self.master.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x500")  # Balanced window size
    app = QuizApp(root)
    root.mainloop()
