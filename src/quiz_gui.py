import tkinter as tk
from tkinter import messagebox, ttk
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
    "bg": "#e8f0fe",
    "accent": "#008080",
    "button": "#7c83fd",
    "button_hover": "#5c6ac4",
    "text": "#1c1c1c",
    "highlight": "#ffd6a5",
}
FONTS = {
    "header": ("Comic Sans MS", 24, "bold"),
    "body": ("Tahoma", 14),
    "button": ("Verdana", 12, "bold"),
}

ADMIN_PASSWORD = "jimmyjenkins"

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
        self.answer_buttons = []


    def show_main_menu(self):
        self.clear_window()

        tk.Label(self.master, text="🌟 Quiz Bowl 🌟", font=FONTS["header"], fg=COLORS["text"], bg=COLORS["bg"]).pack(pady=20)

        tk.Button(self.master, text="Admin Login", command=self.admin_login, bg=COLORS["button"], fg="white",
                  activebackground=COLORS["button_hover"], relief="flat", bd=2, padx=10, pady=5, font=FONTS["button"]).pack(pady=10)

        tk.Button(self.master, text="Take a Quiz!", command=self.show_quiz_selector, bg=COLORS["button"], fg="white",
                  activebackground=COLORS["button_hover"], relief="flat", bd=2, padx=10, pady=5, font=FONTS["button"]).pack(pady=10)

    def show_quiz_selector(self):
        self.clear_window()

        tk.Label(self.master, text="Choose Course Categories", font=FONTS["header"], bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=20)

        self.selected_courses = []
        self.course_vars = {}

        for course in COURSES:
            var = tk.IntVar()
            chk = tk.Checkbutton(self.master, text=course, variable=var, bg=COLORS["bg"], font=FONTS["body"], fg=COLORS["text"])
            chk.pack(anchor='w', padx=40)
            self.course_vars[course] = var

        tk.Button(self.master, text="Start Quiz", command=self.start_quiz, bg=COLORS["button"], fg="white",
                  activebackground=COLORS["button_hover"], relief="flat", bd=2, padx=10, pady=5, font=FONTS["button"]).pack(pady=20)

        tk.Button(self.master, text="Back to Main Menu", command=self.show_main_menu, bg=COLORS["accent"], fg="white", font=FONTS["button"], padx=10, pady=5).pack(pady=10)

    def start_quiz(self):
        self.selected_courses = [c for c, v in self.course_vars.items() if v.get() == 1]
        self.questions = []

        if not self.selected_courses:
            messagebox.showwarning("No Selection", "Please select at least one course.")
            return

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        for course in self.selected_courses:
            table = course.replace(" ", "_").lower()
            cursor.execute(f"SELECT question, option_a, option_b, option_c, option_d, correct_answer FROM {table}")
            self.questions.extend(cursor.fetchall())
        conn.close()

        random.shuffle(self.questions)
        self.questions = self.questions[:10]

        if not self.questions:
            messagebox.showinfo("No Questions", "No questions available in selected courses.")
            return

        self.current_question = 0
        self.score = 0
        self.show_question()

    def show_question(self):
        self.clear_window()
        self.answer_buttons = []  # Reset buttons list each question

        question_data = self.questions[self.current_question]
        question, a, b, c, d, correct = question_data

        tk.Label(self.master, text=f"Question {self.current_question + 1}", font=FONTS["header"], bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=10)
        tk.Label(self.master, text=question, wraplength=500, font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=10)

        for option, value in zip([a, b, c, d], ['A', 'B', 'C', 'D']):
            btn = tk.Button(
                self.master,
                text=f"{value}. {option}",
                command=lambda v=value: self.check_answer(v),
                bg=COLORS["button"],
                fg="white",
                font=FONTS["button"],
                relief="flat",
                padx=10,
                pady=5
            )
            btn.pack(pady=5)
            self.answer_buttons.append(btn)

        self.feedback_label = tk.Label(self.master, text="", font=FONTS["body"], bg=COLORS["bg"])
        self.feedback_label.pack(pady=10)

        tk.Button(self.master, text="Back to Main Menu", command=self.show_main_menu, bg=COLORS["accent"], fg="white",
              font=FONTS["button"], padx=10, pady=5).pack(pady=15)


    def check_answer(self, answer):
        # Disable all buttons
        for btn in self.answer_buttons:
            btn.config(state="disabled")

        correct = self.questions[self.current_question][5]
        is_correct = (answer == correct)
        if is_correct:
            self.score += 1
        self.give_feedback(is_correct)

        #else:
         #   self.show_question()

    def show_score(self):
        self.clear_window()
        tk.Label(self.master, text=f"Your Score: {self.score}/{len(self.questions)}", font=FONTS["header"], bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=30)
        tk.Button(self.master, text="Return to Main Menu", command=self.show_main_menu, bg=COLORS["button"], fg="white", font=FONTS["button"], padx=10, pady=5).pack(pady=20)

    def admin_login(self):
        self.clear_window()
        tk.Label(self.master, text="Admin Login", font=FONTS["header"], bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=20)
        tk.Label(self.master, text="Enter Password:", font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=10)

        self.password_entry = tk.Entry(self.master, show="*", font=FONTS["body"])
        self.password_entry.pack(pady=10)

        tk.Button(self.master, text="Login", command=self.check_admin_password, bg=COLORS["button"], fg="white",
                  activebackground=COLORS["button_hover"], font=FONTS["button"], padx=10, pady=5).pack(pady=20)

        tk.Button(self.master, text="Back to Main Menu", command=self.show_main_menu, bg=COLORS["accent"], fg="white", font=FONTS["button"], padx=10, pady=5).pack(pady=10)

    def check_admin_password(self):
        if self.password_entry.get() == ADMIN_PASSWORD:
            self.show_admin_interface()
        else:
            messagebox.showerror("Access Denied", "Incorrect password.")

    def show_admin_interface(self):
        self.clear_window()
        tk.Label(self.master, text="Admin Interface", font=FONTS["header"], bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=20)

        tk.Button(self.master, text="Add Question", command=self.add_question, bg=COLORS["button"], fg="white",
                  activebackground=COLORS["button_hover"], font=FONTS["button"], padx=10, pady=5).pack(pady=10)

        tk.Button(self.master, text="View Questions", command=self.view_questions, bg=COLORS["button"], fg="white",
                  activebackground=COLORS["button_hover"], font=FONTS["button"], padx=10, pady=5).pack(pady=10)
        
        tk.Button(self.master, text="Edit Question", command=self.edit_question, bg=COLORS["button"], fg="white",
              activebackground=COLORS["button_hover"], font=FONTS["button"], padx=10, pady=5).pack(pady=10)

        tk.Button(self.master, text="Back to Main Menu", command=self.show_main_menu, bg=COLORS["accent"], fg="white", font=FONTS["button"], padx=10, pady=5).pack(pady=20)

    def add_question(self):
        self.clear_window()

        tk.Label(self.master, text="Add New Question", font=FONTS["header"], bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=20)

        # Dropdown for course
        self.add_course_var = tk.StringVar()
        course_dropdown = ttk.Combobox(self.master, textvariable=self.add_course_var, values=COURSES, font=FONTS["body"])
        course_dropdown.set("Select Course")
        course_dropdown.pack(pady=10)

        # Question and answer entries
        self.entries = {}
        fields = ["Question", "Option A", "Option B", "Option C", "Option D", "Correct Answer (A/B/C/D)"]
        for field in fields:
            tk.Label(self.master, text=field + ":", font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"]).pack()
            entry = tk.Entry(self.master, font=FONTS["body"], width=60)
            entry.pack(pady=5)
            self.entries[field] = entry

        tk.Button(self.master, text="Submit", command=self.save_question, bg=COLORS["button"], fg="white",
                font=FONTS["button"], padx=10, pady=5).pack(pady=10)

        tk.Button(self.master, text="Back to Admin Menu", command=self.show_admin_interface, bg=COLORS["accent"], fg="white",
                font=FONTS["button"], padx=10, pady=5).pack(pady=10)
    
    def edit_question(self):
        self.clear_window()

        tk.Label(self.master, text="Edit Existing Question", font=FONTS["header"], bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=20)

        # Dropdown for course
        self.edit_course_var = tk.StringVar()
        course_dropdown = ttk.Combobox(self.master, textvariable=self.edit_course_var, values=COURSES, font=FONTS["body"])
        course_dropdown.set("Select Course")
        course_dropdown.pack(pady=10)

        # Button to load questions for editing
        tk.Button(self.master, text="Load Questions", command=self.load_questions_for_edit, bg=COLORS["button"], fg="white",
                font=FONTS["button"], padx=10, pady=5).pack(pady=10)

        # Return button to Admin Menu
        tk.Button(self.master, text="Back to Admin Menu", command=self.show_admin_interface, bg=COLORS["accent"], fg="white",
                font=FONTS["button"], padx=10, pady=5).pack(pady=10)
        
    def load_questions_for_edit(self):
        course = self.edit_course_var.get()
        if course not in COURSES:
            messagebox.showwarning("Invalid Selection", "Please select a valid course.")
            return

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {course.replace(' ', '_').lower()}")
        rows = cursor.fetchall()
        conn.close()

        # Create a scrollable frame for the list of questions
        scrollable_frame = self.create_scrollable_frame()

        # Display questions
        for row in rows:
            q_id, question, a, b, c, d, correct = row
            question_frame = tk.Frame(scrollable_frame, bg=COLORS["bg"])

            tk.Label(question_frame, text=f"Q: {question}", font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=5)

            # Display answer options
            for opt, val in zip([a, b, c, d], ['A', 'B', 'C', 'D']):
                tk.Label(question_frame, text=f"{val}. {opt}", font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w", padx=20)

            # Button to edit the question
            #tk.Button(question_frame, text="Edit", command=lambda q_id=q_id: self.open_edit_form(q_id), bg=COLORS["accent"], fg="white",
             #       font=FONTS["button"], padx=10, pady=5).pack(pady=5)
            tk.Button(
                question_frame,
                text="Edit",
                command=lambda q_id=q_id, course=course: self.open_edit_form(q_id, course),
                bg=COLORS["accent"],
                fg="white",
                font=FONTS["button"],
                padx=10,
                pady=5
            ).pack(pady=5)

            question_frame.pack(pady=10, padx=20, fill="x")

        # Return button to Admin Menu
        #tk.Button(self.master, text="Back to Admin Menu", command=self.show_admin_interface, bg=COLORS["accent"], fg="white", font=FONTS["button"], padx=10, pady=5).pack(pady=10)

    def open_edit_form(self, q_id, course):
        self.clear_window()

        tk.Label(self.master, text="Edit Question", font=FONTS["header"], bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=20)

        # Fetch the existing question data
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        #cursor.execute(f"SELECT * FROM {COURSES[0].replace(' ', '_').lower()} WHERE id = ?", (q_id,))
        cursor.execute(f"SELECT * FROM {course.replace(' ', '_').lower()} WHERE id = ?", (q_id,))
        row = cursor.fetchone()
        conn.close()

        # Pre-populate the fields with current question data
        question, a, b, c, d, correct = row[1:]

        self.edit_entries = {}
        fields = ["Question", "Option A", "Option B", "Option C", "Option D", "Correct Answer (A/B/C/D)"]
        current_values = [question, a, b, c, d, correct]

        for field, current_value in zip(fields, current_values):
            tk.Label(self.master, text=field + ":", font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"]).pack()
            entry = tk.Entry(self.master, font=FONTS["body"], width=60)
            entry.insert(0, current_value)
            entry.pack(pady=5)
            self.edit_entries[field] = entry

        # Button to save edited question
        tk.Button(self.master, text="Save Changes", command=lambda: self.save_edited_question(q_id, course), bg=COLORS["button"], fg="white",
                font=FONTS["button"], padx=10, pady=5).pack(pady=10)

        # Return button to Admin Menu
        tk.Button(self.master, text="Back to Admin Menu", command=self.show_admin_interface, bg=COLORS["accent"], fg="white", font=FONTS["button"], padx=10, pady=5).pack(pady=10)

    def save_edited_question(self, q_id, course):
        values = {field: self.edit_entries[field].get().strip() for field in self.edit_entries}
        if not all(values.values()):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if values["Correct Answer (A/B/C/D)"] not in ["A", "B", "C", "D"]:
            messagebox.showerror("Error", "Correct answer must be A, B, C, or D.")
            return

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(f"""
            UPDATE {course.replace(' ', '_').lower()} 
            SET question = ?, option_a = ?, option_b = ?, option_c = ?, option_d = ?, correct_answer = ?
            WHERE id = ?
        """, (
            values["Question"],
            values["Option A"],
            values["Option B"],
            values["Option C"],
            values["Option D"],
            values["Correct Answer (A/B/C/D)"],
            q_id
        ))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Question updated successfully!")
        self.show_admin_interface()


            
    def save_question(self):
        course = self.add_course_var.get()
        if course not in COURSES:
            messagebox.showerror("Error", "Please select a valid course.")
            return

        values = {field: self.entries[field].get().strip() for field in self.entries}
        if not all(values.values()):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if values["Correct Answer (A/B/C/D)"] not in ["A", "B", "C", "D"]:
            messagebox.showerror("Error", "Correct answer must be A, B, C, or D.")
            return

        table = course.replace(" ", "_").lower()
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(f"""
            INSERT INTO {table} (question, option_a, option_b, option_c, option_d, correct_answer)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            values["Question"],
            values["Option A"],
            values["Option B"],
            values["Option C"],
            values["Option D"],
            values["Correct Answer (A/B/C/D)"]
        ))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Question added successfully!")
        self.show_admin_interface()



    def view_questions(self):
        self.clear_window()
        tk.Label(self.master, text="View Questions", font=FONTS["header"], fg=COLORS["text"], bg=COLORS["bg"]).pack(pady=20)

        self.course_var = tk.StringVar()
        dropdown = ttk.Combobox(self.master, textvariable=self.course_var, values=COURSES, font=FONTS["body"])
        dropdown.set("Select Course")
        dropdown.pack(pady=10)

        tk.Button(self.master, text="View", command=self.show_questions_for_course, bg=COLORS["button"], fg="white",
                  font=FONTS["button"], padx=10, pady=5).pack(pady=10)

        tk.Button(self.master, text="Back to Admin Menu", command=self.show_admin_interface, bg=COLORS["accent"], fg="white",
                  font=FONTS["button"], padx=10, pady=5).pack(pady=10)

    def show_questions_for_course(self):
        """self.clear_window()

        course = self.course_var.get()
        if course not in COURSES:
            #messagebox.showwarning("Invalid Selection", "Please select a valid course.")
            # Provide a way back to the course selection
            tk.Label(self.master, text="Please select a valid course.", bg=PRIMARY_COLOR, fg=TEXT_COLOR,
                 font=(FONT_FAMILY, FONT_SIZE + 2)).pack(pady=10)

            tk.Button(self.master, text="Back", font=(FONT_FAMILY, FONT_SIZE),
                    bg=BUTTON_COLOR, fg=TEXT_COLOR, command=self.show_admin_interface).pack(pady=10)
            return"""
    
        self.clear_window()

        course = self.course_var.get()
        if course not in COURSES:
            # Display error message
            tk.Label(
                self.master,
                text="Please select a valid course.",
                bg="#ffdddd",          # light red background for warning
                fg="#660000",          # dark red text
                font=("Helvetica", 14, "bold")
            ).pack(pady=10)

            # Back button to return to admin interface
            tk.Button(
                self.master,
                text="Back",
                font=("Helvetica", 12),
                bg="#cc0000",          # red button
                fg="white",
                command=self.show_admin_interface
            ).pack(pady=10)
            return


        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {course.replace(' ', '_').lower()}")
        rows = cursor.fetchall()
        conn.close()

        frame = tk.Frame(self.master, bg=COLORS["bg"])
        canvas = tk.Canvas(frame, bg=COLORS["bg"])
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS["bg"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        frame.pack(fill="both", expand=True)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for row in rows:
            q_id, question, a, b, c, d, correct = row
            tk.Label(scrollable_frame, text=f"Q: {question}", font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"], wraplength=500).pack(pady=5)
            for opt, val in zip([a, b, c, d], ['A', 'B', 'C', 'D']):
                tk.Label(scrollable_frame, text=f"{val}. {opt}", font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"], wraplength=500).pack(anchor="w", padx=20)
            tk.Label(scrollable_frame, text=f"Correct Answer: {correct}", font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=5)
            tk.Button(scrollable_frame, text="Delete", command=lambda r=row: self.delete_question(r), bg=COLORS["accent"], fg="white", font=FONTS["button"], padx=10, pady=5).pack(pady=5)
            tk.Label(scrollable_frame, text="").pack()

        tk.Button(self.master, text="Back to Admin Menu", command=self.show_admin_interface, bg=COLORS["button"], fg="white", font=FONTS["button"], padx=10, pady=5).pack(pady=10)

    def delete_question(self, row):
        course = self.course_var.get()
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {course.replace(' ', '_').lower()} WHERE id = ?", (row[0],))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Question deleted successfully!")
        self.view_questions()

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def create_scrollable_frame(self):
        canvas = tk.Canvas(self.master, bg=COLORS["bg"])
        scrollbar = tk.Scrollbar(self.master, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS["bg"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return scrollable_frame

    
    def give_feedback(self, is_correct):
    # Display feedback text
        feedback_text = "✅ Correct!" if is_correct else f"❌ Incorrect. The correct answer was {self.questions[self.current_question][5]}."
        self.feedback_label.config(text=feedback_text, fg="green" if is_correct else "red")
    
    # Pause for 1.5 seconds before going to the next question
        self.master.after(1500, self.next_question)
    
    def next_question(self):
        self.current_question += 1
        if self.current_question >= len(self.questions):
            self.show_score()
        else:
            self.show_question()



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x600")
    app = QuizApp(root)
    root.mainloop()
