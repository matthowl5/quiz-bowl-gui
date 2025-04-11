import tkinter as tk
from tkinter import messagebox, ttk # ttk is already imported, good!
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
    "accent": "#008080", # Teal
    "button": "#7c83fd", # Primary button color (e.g., Start Quiz, Login)
    "button_hover": "#5c6ac4", # Darker shade for hover/active
    "button_accent": "#008080", # Accent button color (e.g., Back, Delete) - Using accent color
    "button_accent_hover": "#006666", # Darker teal
    "text": "#1c1c1c",
    "highlight": "#ffd6a5",
    "correct": "#28a745", # Green for correct
    "incorrect": "#dc3545", # Red for incorrect
    "entry_bg": "#ffffff", # White background for entry fields
}
FONTS = {
    "header": ("Comic Sans MS", 24, "bold"),
    "body": ("Tahoma", 14),
    "button": ("Verdana", 12, "bold"),
    "feedback": ("Tahoma", 14, "bold"), # Font for feedback label
}

ADMIN_PASSWORD = "jimmyjenkins"

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz Bowl")
        self.master.geometry("600x600") # Set initial size
        # Don't configure master bg directly, use a main frame
        # self.master.configure(bg=COLORS["bg"])

        # --- TTK Styling ---
        self.style = ttk.Style(self.master)
        # Experiment with themes, 'clam' or 'aqua' might look good on Mac
        # Available themes: print(self.style.theme_names())
        try:
            # 'clam' is often more customizable than 'aqua' or 'default'
            self.style.theme_use('clam')
        except tk.TclError:
            print("Clam theme not available, using default.")

        # Configure root style (affects background)
        self.style.configure('.', background=COLORS["bg"], foreground=COLORS["text"])

        # --- Define Custom Widget Styles ---
        self.style.configure("TFrame", background=COLORS["bg"])
        self.style.configure("Header.TLabel", font=FONTS["header"], foreground=COLORS["text"], background=COLORS["bg"], padding=(0, 10, 0, 10)) # top, right, bottom, left
        self.style.configure("Body.TLabel", font=FONTS["body"], foreground=COLORS["text"], background=COLORS["bg"], padding=(5, 5))
        self.style.configure("Feedback.TLabel", font=FONTS["feedback"], background=COLORS["bg"], padding=(10, 10))

        # Button Styles (Background might be tricky with themes, foreground/font more reliable)
        self.style.configure("TButton", font=FONTS["button"], padding=(10, 5), relief="flat", borderwidth=0)
        self.style.map("TButton",
                       foreground=[('!active', 'white'), ('active', 'white')],
                       background=[('!active', COLORS["button"]), ('active', COLORS["button_hover"])])

        # Accent Button Style
        self.style.configure("Accent.TButton", font=FONTS["button"], padding=(10, 5), relief="flat", borderwidth=0)
        self.style.map("Accent.TButton",
                       foreground=[('!active', 'white'), ('active', 'white')],
                       background=[('!active', COLORS["button_accent"]), ('active', COLORS["button_accent_hover"])])

        # Checkbutton Style
        self.style.configure("TCheckbutton", font=FONTS["body"], foreground=COLORS["text"], background=COLORS["bg"], padding=(5, 5))
        self.style.map("TCheckbutton",
                       indicatorcolor=[('selected', COLORS["accent"]), ('!selected', COLORS["text"])])


        # Entry Style
        self.style.configure("TEntry", font=FONTS["body"], padding=(5, 5), fieldbackground=COLORS["entry_bg"])

        # Combobox Style (ensure dropdown list uses theme colors too)
        self.style.configure("TCombobox", font=FONTS["body"], padding=(5,5), fieldbackground=COLORS["entry_bg"])
        # This makes the dropdown list background consistent
        self.master.option_add('*TCombobox*Listbox.background', COLORS["entry_bg"])
        self.master.option_add('*TCombobox*Listbox.foreground', COLORS["text"])
        self.master.option_add('*TCombobox*Listbox.selectBackground', COLORS["accent"])
        self.master.option_add('*TCombobox*Listbox.selectForeground', 'white')


        # --- Main Frame ---
        self.main_frame = ttk.Frame(self.master, padding="10 10 10 10", style="TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # --- App State ---
        self.course = None
        self.questions = []
        self.current_question = 0
        self.score = 0
        self.answer_buttons = []
        self.selected_courses = []
        self.course_vars = {}
        self.entries = {}
        self.edit_entries = {}
        self.add_course_var = tk.StringVar()
        self.edit_course_var = tk.StringVar()
        self.view_course_var = tk.StringVar() # Renamed from self.course_var
        self.password_entry = None
        self.feedback_label = None
        self.scrollable_content_frame = None # To hold widgets in scrollable areas

        self.show_main_menu()


    def clear_window(self):
        # Destroy widgets inside the main_frame, not the main_frame itself
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        # Reset references that might be stale
        self.answer_buttons = []
        self.feedback_label = None
        self.scrollable_content_frame = None


    def show_main_menu(self):
        self.clear_window()

        ttk.Label(self.main_frame, text="🌟 Quiz Bowl 🌟", style="Header.TLabel").pack(pady=20)

        ttk.Button(self.main_frame, text="Admin Login", command=self.admin_login, style="TButton").pack(pady=10)

        ttk.Button(self.main_frame, text="Take a Quiz!", command=self.show_quiz_selector, style="TButton").pack(pady=10)

    def show_quiz_selector(self):
        self.clear_window()

        ttk.Label(self.main_frame, text="Choose Course Categories", style="Header.TLabel").pack(pady=20)

        self.selected_courses = [] # Reset just in case
        self.course_vars = {}

        # Frame to hold checkbuttons for better alignment
        check_frame = ttk.Frame(self.main_frame, style="TFrame")
        check_frame.pack(pady=10)

        for course in COURSES:
            var = tk.IntVar()
            # Use anchor='w' and pack within the check_frame
            chk = ttk.Checkbutton(check_frame, text=course, variable=var, style="TCheckbutton")
            chk.pack(anchor='w', padx=40, pady=2) # Add a little vertical padding
            self.course_vars[course] = var

        ttk.Button(self.main_frame, text="Start Quiz", command=self.start_quiz, style="TButton").pack(pady=20)

        ttk.Button(self.main_frame, text="Back to Main Menu", command=self.show_main_menu, style="Accent.TButton").pack(pady=10)

    def start_quiz(self):
        self.selected_courses = [c for c, v in self.course_vars.items() if v.get() == 1]
        self.questions = []

        if not self.selected_courses:
            messagebox.showwarning("No Selection", "Please select at least one course.", parent=self.master) # Add parent
            return

        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            for course in self.selected_courses:
                table = course.replace(" ", "_").lower()
                cursor.execute(f"SELECT question, option_a, option_b, option_c, option_d, correct_answer FROM {table}")
                self.questions.extend(cursor.fetchall())
            conn.close()
        except sqlite3.Error as e:
             messagebox.showerror("Database Error", f"Failed to load questions: {e}", parent=self.master)
             self.show_main_menu() # Go back if DB fails
             return


        random.shuffle(self.questions)
        self.questions = self.questions[:10] # Limit to 10 questions

        if not self.questions:
            messagebox.showinfo("No Questions", "No questions available in the selected courses.", parent=self.master)
            self.show_quiz_selector() # Go back to selection
            return

        self.current_question = 0
        self.score = 0
        self.show_question()

    def show_question(self):
        self.clear_window()
        self.answer_buttons = []  # Reset buttons list each question

        if not self.questions or self.current_question >= len(self.questions):
             messagebox.showerror("Error", "Could not load question.", parent=self.master)
             self.show_main_menu()
             return

        question_data = self.questions[self.current_question]
        question, a, b, c, d, correct = question_data # correct is 'A', 'B', 'C', or 'D'

        ttk.Label(self.main_frame, text=f"Question {self.current_question + 1}/{len(self.questions)}", style="Header.TLabel").pack(pady=10)
        # Use wraplength for long questions
        ttk.Label(self.main_frame, text=question, wraplength=550, style="Body.TLabel", justify=tk.CENTER).pack(pady=10, padx=10)

        # Frame for answer buttons
        button_frame = ttk.Frame(self.main_frame, style="TFrame")
        button_frame.pack(pady=10)

        options = { 'A': a, 'B': b, 'C': c, 'D': d }
        for value, text in options.items():
            # Create button, assign command with lambda to capture current 'value'
            btn = ttk.Button(
                button_frame,
                text=f"{value}. {text}",
                command=lambda v=value: self.check_answer(v),
                style="TButton",
                width=40 # Make buttons roughly same width
            )
            btn.pack(pady=5, fill=tk.X, padx=20) # Fill horizontally within the button_frame
            self.answer_buttons.append(btn) # Keep track to disable later

        # Label for feedback (correct/incorrect)
        self.feedback_label = ttk.Label(self.main_frame, text="", style="Feedback.TLabel")
        self.feedback_label.pack(pady=10)

        ttk.Button(self.main_frame, text="Back to Main Menu", command=self.show_main_menu, style="Accent.TButton").pack(pady=15)


    def check_answer(self, selected_answer):
        # Disable all answer buttons immediately
        for btn in self.answer_buttons:
            btn.config(state="disabled")

        correct_answer = self.questions[self.current_question][5] # This is 'A', 'B', 'C', or 'D'
        is_correct = (selected_answer == correct_answer)

        if is_correct:
            self.score += 1

        self.give_feedback(is_correct, correct_answer)


    def give_feedback(self, is_correct, correct_answer):
        if self.feedback_label: # Ensure label exists
            if is_correct:
                feedback_text = "✅ Correct!"
                feedback_color = COLORS["correct"]
            else:
                # Find the full text of the correct option
                question_data = self.questions[self.current_question]
                options = {'A': question_data[1], 'B': question_data[2], 'C': question_data[3], 'D': question_data[4]}
                correct_option_text = options.get(correct_answer, "N/A")
                feedback_text = f"❌ Incorrect. The correct answer was {correct_answer}. {correct_option_text}"
                feedback_color = COLORS["incorrect"]

            self.feedback_label.config(text=feedback_text, foreground=feedback_color, wraplength=550) # Use wraplength here too
            # Use foreground directly as ttk.Label doesn't have a simple 'fg' like tk.Label
            # We might need a specific style variation if foreground doesn't work reliably across themes
            # self.style.configure("Correct.Feedback.TLabel", foreground=COLORS["correct"])
            # self.style.configure("Incorrect.Feedback.TLabel", foreground=COLORS["incorrect"])
            # self.feedback_label.config(style="Correct.Feedback.TLabel" if is_correct else "Incorrect.Feedback.TLabel")

        # Pause for 1.5 seconds before going to the next question
        self.master.after(2000, self.next_question) # Increased delay slightly

    def next_question(self):
        self.current_question += 1
        if self.current_question >= len(self.questions):
            self.show_score()
        else:
            self.show_question()

    def show_score(self):
        self.clear_window()
        ttk.Label(self.main_frame, text="Quiz Complete!", style="Header.TLabel").pack(pady=20)
        ttk.Label(self.main_frame, text=f"Your Final Score: {self.score}/{len(self.questions)}", style="Body.TLabel").pack(pady=10)

        percentage = (self.score / len(self.questions)) * 100 if self.questions else 0
        ttk.Label(self.main_frame, text=f"{percentage:.1f}%", style="Body.TLabel").pack(pady=5)

        ttk.Button(self.main_frame, text="Return to Main Menu", command=self.show_main_menu, style="TButton").pack(pady=20)


    # --- Admin Section ---

    def admin_login(self):
        self.clear_window()
        ttk.Label(self.main_frame, text="Admin Login", style="Header.TLabel").pack(pady=20)
        ttk.Label(self.main_frame, text="Enter Password:", style="Body.TLabel").pack(pady=5)

        # Use ttk.Entry
        self.password_entry = ttk.Entry(self.main_frame, show="*", style="TEntry", width=30)
        self.password_entry.pack(pady=10)
        self.password_entry.focus() # Set focus for immediate typing
        # Bind Enter key to login attempt
        self.password_entry.bind("<Return>", self.check_admin_password_event)


        ttk.Button(self.main_frame, text="Login", command=self.check_admin_password, style="TButton").pack(pady=20)
        ttk.Button(self.main_frame, text="Back to Main Menu", command=self.show_main_menu, style="Accent.TButton").pack(pady=10)

    # Helper for Enter key binding
    def check_admin_password_event(self, event=None):
        self.check_admin_password()

    def check_admin_password(self):
        # Check if password_entry exists and has content
        if self.password_entry and self.password_entry.get() == ADMIN_PASSWORD:
            self.show_admin_interface()
        else:
            messagebox.showerror("Access Denied", "Incorrect password.", parent=self.master)
            if self.password_entry:
                 self.password_entry.delete(0, tk.END) # Clear the entry

    def show_admin_interface(self):
        self.clear_window()
        ttk.Label(self.main_frame, text="Admin Interface", style="Header.TLabel").pack(pady=20)

        ttk.Button(self.main_frame, text="Add Question", command=self.add_question, style="TButton").pack(pady=10)
        ttk.Button(self.main_frame, text="View/Delete Questions", command=self.view_questions_select_course, style="TButton").pack(pady=10) # Combined view/delete
        ttk.Button(self.main_frame, text="Edit Question", command=self.edit_question_select_course, style="TButton").pack(pady=10) # Changed command name

        ttk.Button(self.main_frame, text="Back to Main Menu", command=self.show_main_menu, style="Accent.TButton").pack(pady=20)

    def add_question(self):
        self.clear_window()

        ttk.Label(self.main_frame, text="Add New Question", style="Header.TLabel").pack(pady=10) # Reduced padding

        # Use a frame for better layout control
        form_frame = ttk.Frame(self.main_frame, style="TFrame")
        form_frame.pack(pady=5, padx=20, fill=tk.X)

        # Dropdown for course
        ttk.Label(form_frame, text="Course:", style="Body.TLabel").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.add_course_var = tk.StringVar() # Ensure it's initialized here if not in __init__
        course_dropdown = ttk.Combobox(form_frame, textvariable=self.add_course_var, values=COURSES, style="TCombobox", state="readonly") # readonly prevents typing
        course_dropdown.set("Select Course")
        course_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew") # ew = expand east-west

        # Question and answer entries using grid layout
        self.entries = {}
        fields = ["Question", "Option A", "Option B", "Option C", "Option D", "Correct Answer (A/B/C/D)"]
        for i, field in enumerate(fields):
            ttk.Label(form_frame, text=field + ":", style="Body.TLabel").grid(row=i + 1, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(form_frame, style="TEntry", width=60) # Width is approx characters
            entry.grid(row=i + 1, column=1, padx=5, pady=5, sticky="ew")
            self.entries[field] = entry

        # Make the entry column expandable
        form_frame.grid_columnconfigure(1, weight=1)

        # Buttons Frame
        button_frame = ttk.Frame(self.main_frame, style="TFrame")
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Submit", command=self.save_question, style="TButton").pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Back to Admin", command=self.show_admin_interface, style="Accent.TButton").pack(side=tk.LEFT, padx=10)


    def save_question(self):
        course = self.add_course_var.get()
        if not course or course == "Select Course":
            messagebox.showerror("Error", "Please select a valid course.", parent=self.master)
            return

        values = {field: entry.get().strip() for field, entry in self.entries.items()}
        if not all(values.values()):
            messagebox.showerror("Error", "Please fill in all fields.", parent=self.master)
            return

        correct_answer_key = "Correct Answer (A/B/C/D)"
        if values[correct_answer_key].upper() not in ["A", "B", "C", "D"]:
            messagebox.showerror("Error", "Correct answer must be A, B, C, or D.", parent=self.master)
            return

        # Ensure correct answer is uppercase
        values[correct_answer_key] = values[correct_answer_key].upper()

        table = course.replace(" ", "_").lower()
        try:
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
                values[correct_answer_key]
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Question added successfully!", parent=self.master)
            self.show_admin_interface() # Go back after success
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to save question: {e}", parent=self.master)


    # Renamed from edit_question
    def edit_question_select_course(self):
        self.clear_window()
        ttk.Label(self.main_frame, text="Edit Question: Select Course", style="Header.TLabel").pack(pady=20)

        # Dropdown for course
        self.edit_course_var = tk.StringVar() # Ensure it's initialized here if not in __init__
        course_dropdown = ttk.Combobox(self.main_frame, textvariable=self.edit_course_var, values=COURSES, style="TCombobox", state="readonly")
        course_dropdown.set("Select Course")
        course_dropdown.pack(pady=10)

        # Button to load questions for editing
        ttk.Button(self.main_frame, text="Load Questions", command=self.load_questions_for_edit, style="TButton").pack(pady=10)

        # Return button to Admin Menu
        ttk.Button(self.main_frame, text="Back to Admin Menu", command=self.show_admin_interface, style="Accent.TButton").pack(pady=10)

    def load_questions_for_edit(self):
        course = self.edit_course_var.get()
        if not course or course == "Select Course":
            messagebox.showwarning("Invalid Selection", "Please select a valid course.", parent=self.master)
            return

        # Clear current view and show loading message maybe?
        self.clear_window()
        ttk.Label(self.main_frame, text=f"Edit Questions: {course}", style="Header.TLabel").pack(pady=10)

        # Create scrollable area for questions
        self.scrollable_content_frame = self.create_scrollable_frame(self.main_frame) # Pass parent

        rows = []
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            table_name = course.replace(' ', '_').lower()
            cursor.execute(f"SELECT id, question FROM {table_name} ORDER BY id") # Select only id and question for list
            rows = cursor.fetchall()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not load questions: {e}", parent=self.master)
            self.show_admin_interface() # Go back on error
            return

        if not rows:
             ttk.Label(self.scrollable_content_frame, text="No questions found for this course.", style="Body.TLabel").pack(pady=10)
        else:
            # Display questions with Edit buttons
            for q_id, question_text in rows:
                q_frame = ttk.Frame(self.scrollable_content_frame, padding=5, style="TFrame")
                q_frame.pack(fill=tk.X, pady=5, padx=10)

                # Shortened question text for display
                display_text = (question_text[:70] + '...') if len(question_text) > 70 else question_text
                ttk.Label(q_frame, text=f"ID {q_id}: {display_text}", style="Body.TLabel", anchor='w', wraplength=400).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

                # Edit button
                ttk.Button(
                    q_frame,
                    text="Edit",
                    command=lambda q_id=q_id, course=course: self.open_edit_form(q_id, course), # Pass course name too
                    style="Accent.TButton" # Use accent color for edit/delete actions
                ).pack(side=tk.RIGHT, padx=5)


        # Add Back button at the bottom, outside scrollable area
        ttk.Button(self.main_frame, text="Back to Course Selection", command=self.edit_question_select_course, style="Accent.TButton").pack(pady=10, side=tk.BOTTOM)


    def open_edit_form(self, q_id, course): # Added course parameter
        self.clear_window()
        ttk.Label(self.main_frame, text=f"Edit Question ID: {q_id} ({course})", style="Header.TLabel").pack(pady=10)

        # Fetch the existing question data
        row = None
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            table_name = course.replace(' ', '_').lower()
            cursor.execute(f"SELECT question, option_a, option_b, option_c, option_d, correct_answer FROM {table_name} WHERE id = ?", (q_id,))
            row = cursor.fetchone()
            conn.close()
        except sqlite3.Error as e:
             messagebox.showerror("Database Error", f"Failed to fetch question {q_id}: {e}", parent=self.master)
             self.show_admin_interface() # Or back to edit selection?
             return

        if not row:
            messagebox.showerror("Error", f"Question ID {q_id} not found in {course}.", parent=self.master)
            self.load_questions_for_edit() # Refresh the list
            return

        # Pre-populate the fields with current question data
        question, a, b, c, d, correct = row

        # Use a frame for better layout control
        form_frame = ttk.Frame(self.main_frame, style="TFrame")
        form_frame.pack(pady=5, padx=20, fill=tk.X)

        self.edit_entries = {}
        fields = ["Question", "Option A", "Option B", "Option C", "Option D", "Correct Answer (A/B/C/D)"]
        current_values = [question, a, b, c, d, correct]

        for i, (field, current_value) in enumerate(zip(fields, current_values)):
             ttk.Label(form_frame, text=field + ":", style="Body.TLabel").grid(row=i, column=0, padx=5, pady=5, sticky="w")
             entry = ttk.Entry(form_frame, style="TEntry", width=60)
             entry.insert(0, current_value) # Pre-fill
             entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
             self.edit_entries[field] = entry

        # Make the entry column expandable
        form_frame.grid_columnconfigure(1, weight=1)

        # Buttons Frame
        button_frame = ttk.Frame(self.main_frame, style="TFrame")
        button_frame.pack(pady=10)

        # Button to save edited question (pass q_id and course)
        ttk.Button(button_frame, text="Save Changes", command=lambda: self.save_edited_question(q_id, course), style="TButton").pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=self.load_questions_for_edit, style="Accent.TButton").pack(side=tk.LEFT, padx=10) # Go back to the list


    def save_edited_question(self, q_id, course):
        values = {field: entry.get().strip() for field, entry in self.edit_entries.items()}
        if not all(values.values()):
            messagebox.showerror("Error", "Please fill in all fields.", parent=self.master)
            return

        correct_answer_key = "Correct Answer (A/B/C/D)"
        if values[correct_answer_key].upper() not in ["A", "B", "C", "D"]:
            messagebox.showerror("Error", "Correct answer must be A, B, C, or D.", parent=self.master)
            return

        # Ensure correct answer is uppercase
        values[correct_answer_key] = values[correct_answer_key].upper()

        table_name = course.replace(' ', '_').lower()
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE {table_name}
                SET question = ?, option_a = ?, option_b = ?, option_c = ?, option_d = ?, correct_answer = ?
                WHERE id = ?
            """, (
                values["Question"],
                values["Option A"],
                values["Option B"],
                values["Option C"],
                values["Option D"],
                values[correct_answer_key],
                q_id
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Question ID {q_id} updated successfully!", parent=self.master)
            # Go back to the list for that course after saving
            self.load_questions_for_edit()
        except sqlite3.Error as e:
             messagebox.showerror("Database Error", f"Failed to update question: {e}", parent=self.master)


    # Renamed from view_questions
    def view_questions_select_course(self):
        self.clear_window()
        ttk.Label(self.main_frame, text="View/Delete Questions: Select Course", style="Header.TLabel").pack(pady=20)

        self.view_course_var = tk.StringVar() # Renamed from self.course_var
        dropdown = ttk.Combobox(self.main_frame, textvariable=self.view_course_var, values=COURSES, style="TCombobox", state="readonly")
        dropdown.set("Select Course")
        dropdown.pack(pady=10)

        ttk.Button(self.main_frame, text="View", command=self.show_questions_for_course, style="TButton").pack(pady=10)
        ttk.Button(self.main_frame, text="Back to Admin Menu", command=self.show_admin_interface, style="Accent.TButton").pack(pady=10)

    def show_questions_for_course(self):
        course = self.view_course_var.get() # Use the renamed variable
        if not course or course == "Select Course":
             # Show message within the main frame instead of messagebox for non-critical warnings
             self.clear_window()
             ttk.Label(self.main_frame, text="Please select a valid course.", style="Body.TLabel", foreground="red").pack(pady=10)
             # Provide buttons to go back
             ttk.Button(self.main_frame, text="Try Again", command=self.view_questions_select_course, style="TButton").pack(pady=5)
             ttk.Button(self.main_frame, text="Back to Admin", command=self.show_admin_interface, style="Accent.TButton").pack(pady=5)
             return

        # Clear window and add title
        self.clear_window()
        ttk.Label(self.main_frame, text=f"Questions: {course}", style="Header.TLabel").pack(pady=10)

        # Create scrollable frame
        self.scrollable_content_frame = self.create_scrollable_frame(self.main_frame) # Pass parent

        rows = []
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            table_name = course.replace(' ', '_').lower()
            cursor.execute(f"SELECT * FROM {table_name} ORDER BY id") # Get all columns
            rows = cursor.fetchall()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not load questions: {e}", parent=self.master)
            self.show_admin_interface()
            return

        if not rows:
             ttk.Label(self.scrollable_content_frame, text="No questions found for this course.", style="Body.TLabel").pack(pady=10)
        else:
            # Display questions with details and Delete button
            for row in rows:
                q_id, question, a, b, c, d, correct = row

                # Use a Frame for each question entry for better structure
                q_entry_frame = ttk.Frame(self.scrollable_content_frame, style="TFrame", relief=tk.GROOVE, borderwidth=1)
                q_entry_frame.pack(fill=tk.X, pady=5, padx=10)

                # Left frame for text, Right frame for button
                text_frame = ttk.Frame(q_entry_frame, style="TFrame")
                text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
                button_frame = ttk.Frame(q_entry_frame, style="TFrame")
                button_frame.pack(side=tk.RIGHT, padx=5, pady=5)

                # Display details in the left frame
                ttk.Label(text_frame, text=f"ID: {q_id} - Q: {question}", style="Body.TLabel", wraplength=450, anchor="w", justify=tk.LEFT).pack(fill=tk.X)
                details_text = f" A: {a}\n B: {b}\n C: {c}\n D: {d}\n Correct: {correct}"
                ttk.Label(text_frame, text=details_text, style="Body.TLabel", wraplength=450, anchor="w", justify=tk.LEFT).pack(fill=tk.X)

                # Delete button in the right frame
                ttk.Button(button_frame, text="Delete", command=lambda r=row, c=course: self.confirm_delete_question(r, c), style="Accent.TButton").pack()


        # Back button at the bottom, outside scrollable area
        ttk.Button(self.main_frame, text="Back to Course Selection", command=self.view_questions_select_course, style="Accent.TButton").pack(pady=10, side=tk.BOTTOM)


    def confirm_delete_question(self, row, course):
        q_id = row[0]
        question_text = row[1]
        # Ask for confirmation
        response = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete Question ID {q_id}?\n\n'{question_text[:100]}...'",
            parent=self.master
        )
        if response: # If user clicked Yes
            self.delete_question(q_id, course)


    def delete_question(self, q_id, course):
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            table_name = course.replace(' ', '_').lower()
            cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (q_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Question ID {q_id} deleted successfully!", parent=self.master)
            # Refresh the view for the current course
            self.show_questions_for_course()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to delete question ID {q_id}: {e}", parent=self.master)


    # --- Utility Methods ---

    def create_scrollable_frame(self, parent):
        # Use tk.Canvas and tk.Scrollbar as ttk versions aren't standard/needed here
        # Container frame to hold canvas and scrollbar
        container = ttk.Frame(parent, style="TFrame")
        container.pack(fill=tk.BOTH, expand=True) # Make container fill space

        canvas = tk.Canvas(container, bg=COLORS["bg"], highlightthickness=0) # Use tk.Canvas
        # Use ttk scrollbar for better theme integration if available
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        # Frame inside the canvas where the actual content goes (use ttk.Frame)
        scrollable_frame = ttk.Frame(canvas, style="TFrame")

        # When the scrollable_frame size changes, update the scrollregion
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Create the window on the canvas to display the scrollable_frame
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Configure the canvas to use the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar into the container
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mouse wheel scrolling (important for usability)
        # Platform-specific bindings
        def _on_mousewheel(event):
             # Determine scroll direction and amount (differs slightly by platform)
            if event.num == 5 or event.delta < 0: # Scroll down (Linux uses 5, others use negative delta)
                 canvas.yview_scroll(1, "units")
            elif event.num == 4 or event.delta > 0: # Scroll up (Linux uses 4, others use positive delta)
                 canvas.yview_scroll(-1, "units")

        # Bind for different platforms
        canvas.bind_all("<MouseWheel>", _on_mousewheel) # Windows, MacOS
        canvas.bind_all("<Button-4>", _on_mousewheel)   # Linux scroll up
        canvas.bind_all("<Button-5>", _on_mousewheel)   # Linux scroll down
        # Also bind to the inner frame to catch events there too
        scrollable_frame.bind_all("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind_all("<Button-4>", _on_mousewheel)
        scrollable_frame.bind_all("<Button-5>", _on_mousewheel)


        return scrollable_frame # Return the frame where content should be placed



if __name__ == "__main__":
    # Simple DB Initialization (Create tables if they don't exist)
    def initialize_db():
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        for course in COURSES:
            table_name = course.replace(" ", "_").lower()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    option_a TEXT NOT NULL,
                    option_b TEXT NOT NULL,
                    option_c TEXT NOT NULL,
                    option_d TEXT NOT NULL,
                    correct_answer TEXT NOT NULL CHECK(correct_answer IN ('A', 'B', 'C', 'D'))
                )
            """)
        conn.commit()
        conn.close()

    initialize_db() # Ensure tables exist before starting app

    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()