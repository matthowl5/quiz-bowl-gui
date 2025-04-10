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
    "bg": "#e8f0fe",           # Soft blue-gray (background)
    "accent": "#008080",       # Teal (accent)
    "button": "#7c83fd",       # Deep lavender (buttons)
    "button_hover": "#5c6ac4", # Slate blue (hover)
    "text": "#1c1c1c",         # Charcoal black (text)
    "highlight": "#ffd6a5",    # Light peach (selection highlight)
}
FONTS = {
    "header": ("Comic Sans MS", 24, "bold"),
    "body": ("Tahoma", 14),
    "button": ("Verdana", 12, "bold"),
}

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz Bowl")
        self.master.configure(bg=COLORS["bg"])
        self.course = None
        self.questions = []
        self.current_question = 0
        self.score = 0
        self.show_course_selection()

    def show_course_selection(self):
        self.clear_window()

        tk.Label(self.master, text="🌟 Quiz Bowl 🌟", font=FONTS["header"],
                 fg=COLORS["text"], bg=COLORS["bg"]).pack(pady=20)

        tk.Label(self.master, text="Choose a course category:", font=FONTS["body"],
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=10)

        for course in COURSES:
            btn = tk.Button(
                self.master, text=course, command=lambda c=course: self.start_quiz(c),
                bg=COLORS["button"], fg="white", activebackground=COLORS["button_hover"],
                relief="flat", bd=2, padx=10, pady=5, font=FONTS["button"]
            )
            btn.pack(pady=6, ipadx=10)

    def start_quiz(self, course):
        self.course = course
        self.questions = self.get_questions(course)
        if not self.questions:
            messagebox.showinfo("No Questions", "This category has no questions yet.")
            return
        self.current_question = 0
        self.score = 0
        self.show_question()

    def get_questions(self, course):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {course.replace(' ', '_').lower()}")
        rows = cursor.fetchall()
        conn.close()
        random.shuffle(rows)
        return rows

    def show_question(self):
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
        selected = self.selected.get()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an answer.")
            return
        if selected == self.correct_answer:
            self.score += 1
        self.current_question += 1
        self.show_question()

    def show_score(self):
        self.clear_window()

        total = len(self.questions)
        percentage = (self.score / total) * 100
        if percentage >= 90:
            emoji = "🏆"
        elif percentage >= 70:
            emoji = "😀"
        elif percentage >= 50:
            emoji = "😐"
        else:
            emoji = "😢"

        tk.Label(
            self.master,
            text=f"{emoji} Your Score: {self.score} / {total}",
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
        for widget in self.master.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x500")
    app = QuizApp(root)
    root.mainloop()
