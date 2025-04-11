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

ADMIN_PASSWORD = "jimmyjenkins"  # Admin password

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz Bowl")
        self.master.configure(bg=COLORS["bg"])
        self.course = None
        self.questions = []
        self.current_question = 0
        self.score = 0
        self.show_main_menu()

    def show_main_menu(self):
        self.clear_window()

        tk.Label(self.master, text="🌟 Quiz Bowl 🌟", font=FONTS["header"],
                 fg=COLORS["text"], bg=COLORS["bg"]).pack(pady=20)

        tk.Button(
            self.master, text="Admin Login", command=self.admin_login,
            bg=COLORS["button"], fg="white", activebackground=COLORS["button_hover"],
            relief="flat", bd=2, padx=10, pady=5, font=FONTS["button"]
        ).pack(pady=10)

        tk.Label(self.master, text="Choose a course category:", font=FONTS["body"],
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=10)

        for course in COURSES:
            btn = tk.Button(
                self.master, text=course, command=lambda c=course: self.start_quiz(c),
                bg=COLORS["button"], fg="white", activebackground=COLORS["button_hover"],
                relief="flat", bd=2, padx=10, pady=5, font=FONTS["button"]
            )
            btn.pack(pady=6, ipadx=10)

    def admin_login(self):
        self.clear_window()
        tk.Label(self.master, text="Admin Login", font=FONTS["header"], fg=COLORS["text"], bg=COLORS["bg"]).pack(pady=20)

        tk.Label(self.master, text="Enter Password:", font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=10)

        self.password_entry = tk.Entry(self.master, show="*", font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"])
        self.password_entry.pack(pady=10)

        tk.Button(
            self.master, text="Login", command=self.check_admin_password,
            bg=COLORS["button"], fg="white", activebackground=COLORS["button_hover"],
            relief="flat", bd=2, padx=10, pady=5, font=FONTS["button"]
        ).pack(pady=20)

    def check_admin_password(self):
        password = self.password_entry.get()
        if password == ADMIN_PASSWORD:
            self.show_admin_interface()
        else:
            messagebox.showerror("Access Denied", "Incorrect password.")

    def show_admin_interface(self):
        self.clear_window()
        tk.Label(self.master, text="Admin Interface", font=FONTS["header"], fg=COLORS["text"], bg=COLORS["bg"]).pack(pady=20)

        tk.Button(
            self.master, text="Add Question", command=self.add_question,
            bg=COLORS["button"], fg="white", activebackground=COLORS["button_hover"],
            relief="flat", bd=2, padx=10, pady=5, font=FONTS["button"]
        ).pack(pady=10)

        tk.Button(
            self.master, text="View Questions", command=self.view_questions,
            bg=COLORS["button"], fg="white", activebackground=COLORS["button_hover"],
            relief="flat", bd=2, padx=10, pady=5, font=FONTS["button"]
        ).pack(pady=10)

        tk.Button(
            self.master, text="Back to Main Menu", command=self.show_main_menu,
            bg=COLORS["accent"], fg="white", font=FONTS["button"], padx=10, pady=5
        ).pack(pady=10)

    def add_question(self):
        self.clear_window()
        tk.Label(self.master, text="Add New Question", font=FONTS["header"], fg=COLORS["text"], bg=COLORS["bg"]).pack(pady=20)

        self.course_label = tk.Label(self.master, text="Select Course:", font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"])
        self.course_label.pack(pady=10)

        self.course_var = tk.StringVar()
        self.course_dropdown = tk.OptionMenu(self.master, self.course_var, *COURSES)
        self.course_dropdown.pack(pady=10)

        self.question_label = tk.Label(self.master, text="Enter Question:", font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"])
        self.question_label.pack(pady=10)

        self.question_entry = tk.Entry(self.master, font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"])
        self.question_entry.pack(pady=10)

        self.option_labels = []
        self.option_entries = []
        for i in range(4):
            label = tk.Label(self.master, text=f"Option {chr(65 + i)}:", font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"])
            label.pack(pady=5)
            entry = tk.Entry(self.master, font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"])
            entry.pack(pady=5)
            self.option_labels.append(label)
            self.option_entries.append(entry)

        self.correct_answer_label = tk.Label(self.master, text="Correct Answer (A/B/C/D):", font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"])
        self.correct_answer_label.pack(pady=10)

        self.correct_answer_entry = tk.Entry(self.master, font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"])
        self.correct_answer_entry.pack(pady=10)

        tk.Button(
            self.master, text="Submit Question", command=self.submit_question,
            bg=COLORS["button"], fg="white", activebackground=COLORS["button_hover"],
            relief="flat", bd=2, padx=10, pady=5, font=FONTS["button"]
        ).pack(pady=20)

    def submit_question(self):
        course = self.course_var.get()
        question = self.question_entry.get()
        options = [entry.get() for entry in self.option_entries]
        correct_answer = self.correct_answer_entry.get().upper()

        if not course or not question or not all(options) or correct_answer not in ['A', 'B', 'C', 'D']:
            messagebox.showerror("Invalid Input", "Please fill all fields and provide a valid answer (A/B/C/D).")
            return

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {course.replace(' ', '_').lower()} (question, option_a, option_b, option_c, option_d, correct_answer) VALUES (?, ?, ?, ?, ?, ?)",
                       (question, *options, correct_answer))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Question added successfully!")
        self.show_admin_interface()

    def view_questions(self):
        self.clear_window()
        tk.Label(self.master, text="View Questions", font=FONTS["header"], fg=COLORS["text"], bg=COLORS["bg"]).pack(pady=20)

        self.course_label = tk.Label(self.master, text="Select Course:", font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"])
        self.course_label.pack(pady=10)

        self.course_var = tk.StringVar()
        self.course_dropdown = tk.OptionMenu(self.master, self.course_var, *COURSES)
        self.course_dropdown.pack(pady=10)

        tk.Button(
            self.master, text="View Questions", command=self.show_questions_for_course,
            bg=COLORS["button"], fg="white", activebackground=COLORS["button_hover"],
            relief="flat", bd=2, padx=10, pady=5, font=FONTS["button"]
        ).pack(pady=20)

    def show_questions_for_course(self):
        course = self.course_var.get()

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {course.replace(' ', '_').lower()}")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            messagebox.showinfo("No Questions", "There are no questions in this course.")
            return

        self.clear_window()

        tk.Label(self.master, text=f"Questions for {course}", font=FONTS["header"], fg=COLORS["text"], bg=COLORS["bg"]).pack(pady=20)

        for row in rows:
            question_text = row[1]
            options = row[2:6]
            correct_answer = row[6]

            tk.Label(self.master, text=f"Q: {question_text}", font=FONTS["body"], fg=COLORS["text"], bg=COLORS["bg"]).pack(pady=5)
            for i, option in zip(["A", "B", "C", "D"], options):
                tk.Label(self.master, text=f"{i}. {option}", font=FONTS["body"], fg=COLORS["text"], bg=COLORS["bg"]).pack(pady=2)

            tk.Label(self.master, text=f"Correct Answer: {correct_answer}", font=FONTS["body"], fg=COLORS["text"], bg=COLORS["bg"]).pack(pady=10)

            tk.Button(
                self.master, text="Delete", command=lambda r=row: self.delete_question(r),
                bg=COLORS["accent"], fg="white", font=FONTS["button"], padx=10, pady=5
            ).pack(pady=5)

            tk.Button(
                self.master, text="Edit", command=lambda r=row: self.edit_question(r),
                bg=COLORS["button"], fg="white", font=FONTS["button"], padx=10, pady=5
            ).pack(pady=5)

        tk.Button(
            self.master, text="Back to Admin Menu", command=self.show_admin_interface,
            bg=COLORS["button"], fg="white", font=FONTS["button"], padx=10, pady=5
        ).pack(pady=10)

    def delete_question(self, row):
        course = self.course_var.get()
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {course.replace(' ', '_').lower()} WHERE id = ?", (row[0],))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Question deleted successfully!")
        self.view_questions()

    def edit_question(self, row):
        # Placeholder for the Edit functionality, which could involve updating the question or options.
        messagebox.showinfo("Edit Question", "This feature allows editing of existing questions.")
    
    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x500")
    app = QuizApp(root)
    root.mainloop()
