# gui.py

import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from hash_table import HashTable
from student import Student
from utils import save_to_file, load_from_file, sort_grades, grade_statistics
from tooltips import ToolTip
import os  # Ensure os is imported if used
import sys

class StudentManagementApp:
    def __init__(self, root):
        """
        Initialize the Student Management Application.

        Args:
            root (ttk.Window): The root window of the Tkinter application.
        """
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1000x800")

        # Set ttkbootstrap theme
        self.style = ttk.Style("superhero")  # Choose from available themes like 'cosmo', 'flatly', 'superhero', etc.

        # Initialize HashTable and load existing data
        self.hash_table = HashTable()
        load_from_file(self.hash_table)  # Ensure default filename is used correctly

        # Create the GUI widgets
        self.create_widgets()

        # Handle the window close event to ensure data is saved
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Start auto-save every 5 minutes (300,000 milliseconds)
        self.root.after(300000, self.auto_save)

    def create_widgets(self):
        """
        Create and organize all GUI components within tabs.
        """
        # Create a top frame for the title
        top_frame = ttk.Frame(self.root)
        top_frame.pack(side='top', fill='x', pady=10)

        # Title Label
        title_label = ttk.Label(top_frame, text="Student Management System", font=('Helvetica', 16, 'bold'), bootstyle='inverse-primary')
        title_label.pack()

        # Create a menu bar
        menubar = ttk.Menu(self.root)

        # File Menu
        file_menu = ttk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save As...", command=self.save_data_as, accelerator="Ctrl+Shift+S")
        file_menu.add_command(label="Load From...", command=self.load_data_from, accelerator="Ctrl+Shift+L")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing, accelerator="Ctrl+Q")
        menubar.add_cascade(label="File", menu=file_menu)

        # Theme Menu
        theme_menu = ttk.Menu(menubar, tearoff=0)
        themes = ['superhero', 'flatly', 'cosmo', 'darkly', 'litera', 'pulse', 'journal', 'morph', 'solar']
        for theme in themes:
            theme_menu.add_command(label=theme.capitalize(), command=lambda t=theme: self.change_theme(t))
        menubar.add_cascade(label="Themes", menu=theme_menu)

        # Help Menu
        help_menu = ttk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        # Configure the menu
        self.root.config(menu=menubar)

        # Bind keyboard shortcuts
        self.root.bind_all("<Control-Shift-s>", lambda event: self.save_data_as())
        self.root.bind_all("<Control-Shift-l>", lambda event: self.load_data_from())
        self.root.bind_all("<Control-q>", lambda event: self.on_closing())

        # Create Tabs using ttk.Notebook
        tab_control = ttk.Notebook(self.root)

        # Define individual tabs
        self.tab_add_student = ttk.Frame(tab_control)
        self.tab_delete_student = ttk.Frame(tab_control)
        self.tab_retrieve_student = ttk.Frame(tab_control)
        self.tab_manage_grades = ttk.Frame(tab_control)
        self.tab_display = ttk.Frame(tab_control)
        self.tab_statistics = ttk.Frame(tab_control)

        # Add tabs to the notebook
        tab_control.add(self.tab_add_student, text='Add Student')
        tab_control.add(self.tab_delete_student, text='Delete Student')
        tab_control.add(self.tab_retrieve_student, text='Retrieve Student')
        tab_control.add(self.tab_manage_grades, text='Manage Grades')
        tab_control.add(self.tab_display, text='Display All Students')
        tab_control.add(self.tab_statistics, text='Statistics')

        # Pack the notebook to fill the window
        tab_control.pack(expand=1, fill='both')

        # Initialize each tab's content
        self.create_add_student_tab()
        self.create_delete_student_tab()
        self.create_retrieve_student_tab()
        self.create_manage_grades_tab()
        self.create_display_tab()
        self.create_statistics_tab()

        # Create a status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Welcome to the Student Management System!")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief='sunken', anchor='w', bootstyle='light')
        status_bar.pack(side='bottom', fill='x')

    def create_add_student_tab(self):
        """
        Create the 'Add Student' tab with input fields and an add button.
        """
        frame = self.tab_add_student

        # Create a sub-frame for input fields with padding
        input_frame = ttk.Frame(frame, padding="20")
        input_frame.pack(fill='x', expand=True)

        # Configure grid layout with appropriate padding
        input_frame.columnconfigure(0, weight=1, pad=10)
        input_frame.columnconfigure(1, weight=3, pad=10)

        # Labels and Entry Fields with Padding and ToolTips
        ttk.Label(input_frame, text="Student ID:", font=('Helvetica', 10, 'bold')).grid(column=0, row=0, padx=5, pady=5, sticky='E')
        self.entry_id = ttk.Entry(input_frame, width=30, bootstyle='success')
        self.entry_id.grid(column=1, row=0, padx=5, pady=5, sticky='W')
        ToolTip(self.entry_id, "Enter a unique identifier for the student.")

        ttk.Label(input_frame, text="Name:", font=('Helvetica', 10, 'bold')).grid(column=0, row=1, padx=5, pady=5, sticky='E')
        self.entry_name = ttk.Entry(input_frame, width=30, bootstyle='success')
        self.entry_name.grid(column=1, row=1, padx=5, pady=5, sticky='W')
        ToolTip(self.entry_name, "Enter the student's full name.")

        ttk.Label(input_frame, text="Gender:", font=('Helvetica', 10, 'bold')).grid(column=0, row=2, padx=5, pady=5, sticky='E')
        self.gender_var = tk.StringVar(value="Select")
        genders = ["Male", "Female", "Other"]
        gender_frame = ttk.Frame(input_frame)
        gender_frame.grid(column=1, row=2, padx=5, pady=5, sticky='W')
        for gender in genders:
            ttk.Radiobutton(gender_frame, text=gender, variable=self.gender_var, value=gender).pack(side='left', padx=5)
        ToolTip(gender_frame, "Select the student's gender.")

        ttk.Label(input_frame, text="Age:", font=('Helvetica', 10, 'bold')).grid(column=0, row=3, padx=5, pady=5, sticky='E')
        vcmd = (self.root.register(self.validate_age), '%P')
        self.entry_age = ttk.Entry(input_frame, width=30, bootstyle='success', validate='key', validatecommand=vcmd)
        self.entry_age.grid(column=1, row=3, padx=5, pady=5, sticky='W')
        ToolTip(self.entry_age, "Enter the student's age as a positive integer.")

        # Add Button
        btn_add = ttk.Button(input_frame, text="Add Student", command=self.add_student, bootstyle='primary-outline')
        btn_add.grid(column=1, row=4, padx=5, pady=15, sticky='E')
        ToolTip(btn_add, "Click to add the student to the system.")

    def validate_age(self, P):
        """
        Validate that the age entry contains only positive integers.

        Args:
            P (str): The proposed value of the entry.

        Returns:
            bool: True if valid, False otherwise.
        """
        if P.isdigit() and int(P) > 0:
            return True
        elif P == "":
            return True
        else:
            return False

    def add_student(self):
        """
        Add a new student to the hash table after validating inputs.
        """
        student_id = self.entry_id.get().strip()
        name = self.entry_name.get().strip()
        gender = self.gender_var.get()
        age = self.entry_age.get().strip()

        if not (student_id and name and gender and age):
            messagebox.showerror("Input Error", "All fields are required.")
            self.status_var.set("Failed to add student: Incomplete information.")
            return

        try:
            age = int(age)
            if age <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Age must be a positive integer.")
            self.status_var.set("Failed to add student: Invalid age.")
            return

        # Check if student_id is unique
        if self.hash_table.retrieve(student_id):
            messagebox.showerror("Duplicate ID", f"Student ID '{student_id}' already exists.")
            self.status_var.set("Failed to add student: Duplicate ID.")
            return

        # Create and insert the new student
        student = Student(student_id, name, gender, age)
        success = self.hash_table.insert(student.student_id, student)
        if success:
            messagebox.showinfo("Success", f"Student '{name}' with ID '{student_id}' added successfully.")
            self.status_var.set(f"Added student '{name}' with ID '{student_id}'.")
            # Clear entry fields
            self.entry_id.delete(0, tk.END)
            self.entry_name.delete(0, tk.END)
            self.gender_var.set("Select")
            self.entry_age.delete(0, tk.END)
        else:
            messagebox.showerror("Error", f"Failed to add student '{name}'.")
            self.status_var.set(f"Failed to add student '{name}'.")

    def create_delete_student_tab(self):
        """
        Create the 'Delete Student' tab with input fields for student ID and a delete button.
        """
        frame = self.tab_delete_student

        # Create a sub-frame for input fields with padding
        input_frame = ttk.Frame(frame, padding="20")
        input_frame.pack(fill='x', expand=True)

        # Configure grid layout with appropriate padding
        input_frame.columnconfigure(0, weight=1, pad=10)
        input_frame.columnconfigure(1, weight=3, pad=10)

        # Labels and Entry Fields with Padding and ToolTips
        ttk.Label(input_frame, text="Student ID:", font=('Helvetica', 10, 'bold')).grid(column=0, row=0, padx=5, pady=5, sticky='E')
        self.entry_delete_id = ttk.Entry(input_frame, width=30, bootstyle='danger')
        self.entry_delete_id.grid(column=1, row=0, padx=5, pady=5, sticky='W')
        ToolTip(self.entry_delete_id, "Enter the student's ID to delete.")

        # Delete Button
        btn_delete = ttk.Button(input_frame, text="Delete Student", command=self.delete_student, bootstyle='danger-outline')
        btn_delete.grid(column=1, row=1, padx=5, pady=15, sticky='E')
        ToolTip(btn_delete, "Click to delete the specified student.")

    def delete_student(self):
        """
        Delete a student from the hash table based on student ID.
        """
        student_id = self.entry_delete_id.get().strip()

        if not student_id:
            messagebox.showerror("Input Error", "Student ID is required.")
            self.status_var.set("Failed to delete student: Student ID not provided.")
            return

        student = self.hash_table.retrieve(student_id)

        if student:
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete student '{student.name}' with ID '{student_id}'?")
            if confirm:
                success = self.hash_table.delete(student_id)
                if success:
                    messagebox.showinfo("Success", f"Student '{student.name}' with ID '{student_id}' deleted successfully.")
                    self.status_var.set(f"Deleted student '{student.name}' with ID '{student_id}'.")
                    self.entry_delete_id.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", f"Failed to delete student '{student.name}' with ID '{student_id}'.")
                    self.status_var.set(f"Failed to delete student '{student.name}' with ID '{student_id}'.")
        else:
            messagebox.showerror("Not Found", f"Student with ID '{student_id}' not found.")
            self.status_var.set(f"Failed to delete student: ID '{student_id}' not found.")

    def create_retrieve_student_tab(self):
        """
        Create the 'Retrieve Student' tab with input field for student ID and a retrieve button.
        """
        frame = self.tab_retrieve_student

        # Create a sub-frame for input fields with padding
        input_frame = ttk.Frame(frame, padding="20")
        input_frame.pack(fill='x', expand=True)

        # Configure grid layout with appropriate padding
        input_frame.columnconfigure(0, weight=1, pad=10)
        input_frame.columnconfigure(1, weight=3, pad=10)

        # Labels and Entry Fields with Padding and ToolTips
        ttk.Label(input_frame, text="Student ID:", font=('Helvetica', 10, 'bold')).grid(column=0, row=0, padx=5, pady=5, sticky='E')
        self.entry_retrieve_id = ttk.Entry(input_frame, width=30, bootstyle='info')
        self.entry_retrieve_id.grid(column=1, row=0, padx=5, pady=5, sticky='W')
        ToolTip(self.entry_retrieve_id, "Enter the student's ID to retrieve information.")

        # Retrieve Button
        btn_retrieve = ttk.Button(input_frame, text="Retrieve Student", command=self.retrieve_student, bootstyle='info-outline')
        btn_retrieve.grid(column=1, row=1, padx=5, pady=15, sticky='E')
        ToolTip(btn_retrieve, "Click to retrieve the student's information.")

        # Create a Text widget with Scrollbar to display student information
        display_frame = ttk.Frame(frame, padding="20")
        display_frame.pack(fill='both', expand=True)

        scrollbar = ttk.Scrollbar(display_frame, orient='vertical')
        self.text_retrieve = tk.Text(display_frame, width=100, height=25, yscrollcommand=scrollbar.set, font=('Segoe UI', 10))
        scrollbar.config(command=self.text_retrieve.yview)
        scrollbar.pack(side='right', fill='y')
        self.text_retrieve.pack(side='left', fill='both', expand=True)
        ToolTip(self.text_retrieve, "Displays the retrieved student information.")

    def retrieve_student(self):
        """
        Retrieve and display student information based on the entered student ID.
        """
        student_id = self.entry_retrieve_id.get().strip()

        if not student_id:
            messagebox.showerror("Input Error", "Student ID is required.")
            self.status_var.set("Failed to retrieve student: Student ID not provided.")
            return

        student = self.hash_table.retrieve(student_id)

        self.text_retrieve.delete('1.0', tk.END)

        if student:
            grades = student.grades
            if grades:
                grades_info = "\n".join([f"{course}: {grade}" for course, grade in grades.items()])
                info = (
                    f"Student ID: {student.student_id}\n"
                    f"Name: {student.name}\n"
                    f"Gender: {student.gender}\n"
                    f"Age: {student.age}\n"
                    f"Grades:\n{grades_info}\n"
                    f"Total Grades: {student.total_grade()}\n"
                    f"{'-'*40}\n"
                )
            else:
                info = (
                    f"Student ID: {student.student_id}\n"
                    f"Name: {student.name}\n"
                    f"No grades recorded.\n"
                    f"{'-'*40}\n"
                )
            self.text_retrieve.insert(tk.END, info)
            self.status_var.set(f"Retrieved information for student '{student.name}'.")
        else:
            self.text_retrieve.insert(tk.END, f"Student with ID '{student_id}' not found.")
            self.status_var.set(f"Failed to retrieve student: ID '{student_id}' not found.")

    def create_manage_grades_tab(self):
        """
        Create the 'Manage Grades' tab with functionalities to add and view grades.
        """
        frame = self.tab_manage_grades

        # Create a sub-frame for adding grades
        add_grade_frame = ttk.LabelFrame(frame, text="Add Grades", padding="20")
        add_grade_frame.pack(fill='x', expand=True, padx=10, pady=10)

        # Configure grid layout with appropriate padding
        add_grade_frame.columnconfigure(0, weight=1, pad=10)
        add_grade_frame.columnconfigure(1, weight=3, pad=10)

        # Labels and Entry Fields with Padding and ToolTips
        ttk.Label(add_grade_frame, text="Student ID:", font=('Helvetica', 10, 'bold')).grid(column=0, row=0, padx=5, pady=5, sticky='E')
        self.entry_grade_id = ttk.Entry(add_grade_frame, width=30, bootstyle='warning')
        self.entry_grade_id.grid(column=1, row=0, padx=5, pady=5, sticky='W')
        ToolTip(self.entry_grade_id, "Enter the student's ID to add grades.")

        ttk.Label(add_grade_frame, text="Course Name:", font=('Helvetica', 10, 'bold')).grid(column=0, row=1, padx=5, pady=5, sticky='E')
        self.entry_course = ttk.Entry(add_grade_frame, width=30, bootstyle='warning')
        self.entry_course.grid(column=1, row=1, padx=5, pady=5, sticky='W')
        ToolTip(self.entry_course, "Enter the course name.")

        ttk.Label(add_grade_frame, text="Grade:", font=('Helvetica', 10, 'bold')).grid(column=0, row=2, padx=5, pady=5, sticky='E')
        vcmd_grade = (self.root.register(self.validate_grade), '%P')
        self.entry_grade = ttk.Entry(add_grade_frame, width=30, bootstyle='warning', validate='key', validatecommand=vcmd_grade)
        self.entry_grade.grid(column=1, row=2, padx=5, pady=5, sticky='W')
        ToolTip(self.entry_grade, "Enter the grade (0-100).")

        # Add Grade Button
        btn_add_grade = ttk.Button(add_grade_frame, text="Add Grade", command=self.add_grade, bootstyle='warning-outline')
        btn_add_grade.grid(column=1, row=3, padx=5, pady=15, sticky='E')
        ToolTip(btn_add_grade, "Click to add the grade to the student.")

        # Create a sub-frame for viewing grades
        view_grade_frame = ttk.LabelFrame(frame, text="View Grades", padding="20")
        view_grade_frame.pack(fill='x', expand=True, padx=10, pady=10)

        # Configure grid layout with appropriate padding
        view_grade_frame.columnconfigure(0, weight=1, pad=10)
        view_grade_frame.columnconfigure(1, weight=3, pad=10)

        ttk.Label(view_grade_frame, text="Student ID:", font=('Helvetica', 10, 'bold')).grid(column=0, row=0, padx=5, pady=5, sticky='E')
        self.entry_view_grades_id = ttk.Entry(view_grade_frame, width=30, bootstyle='info')
        self.entry_view_grades_id.grid(column=1, row=0, padx=5, pady=5, sticky='W')
        ToolTip(self.entry_view_grades_id, "Enter the student's ID to view grades.")

        # View Grades Button
        btn_view_grades = ttk.Button(view_grade_frame, text="View Grades", command=self.view_grades, bootstyle='info-outline')
        btn_view_grades.grid(column=1, row=1, padx=5, pady=15, sticky='E')
        ToolTip(btn_view_grades, "Click to view the student's grades.")

        # Create a Text widget with Scrollbar to display grades
        display_frame = ttk.Frame(frame, padding="20")
        display_frame.pack(fill='both', expand=True)

        scrollbar = ttk.Scrollbar(display_frame, orient='vertical')
        self.text_grades = tk.Text(display_frame, width=100, height=15, yscrollcommand=scrollbar.set, font=('Segoe UI', 10))
        scrollbar.config(command=self.text_grades.yview)
        scrollbar.pack(side='right', fill='y')
        self.text_grades.pack(side='left', fill='both', expand=True)
        ToolTip(self.text_grades, "Displays the student's grades.")

    def validate_grade(self, P):
        """
        Validate that the grade entry contains only numbers between 0 and 100.

        Args:
            P (str): The proposed value of the entry.

        Returns:
            bool: True if valid, False otherwise.
        """
        if P == "":
            return True
        try:
            grade = float(P)
            if 0 <= grade <= 100:
                return True
            else:
                return False
        except ValueError:
            return False

    def add_grade(self):
        """
        Add a grade to a student's record after validating inputs.
        """
        student_id = self.entry_grade_id.get().strip()
        course = self.entry_course.get().strip()
        grade = self.entry_grade.get().strip()

        if not (student_id and course and grade):
            messagebox.showerror("Input Error", "All fields are required.")
            self.status_var.set("Failed to add grade: Incomplete information.")
            return

        try:
            grade = float(grade)
            if grade < 0 or grade > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Grade must be a number between 0 and 100.")
            self.status_var.set("Failed to add grade: Invalid grade.")
            return

        student = self.hash_table.retrieve(student_id)

        if student:
            student.add_grade(course, grade)
            messagebox.showinfo("Success", f"Grade for course '{course}' added to student '{student.name}'.")
            self.status_var.set(f"Added grade for course '{course}' to student '{student.name}'.")
        else:
            messagebox.showerror("Not Found", f"Student with ID '{student_id}' not found.")
            self.status_var.set(f"Failed to add grade: Student ID '{student_id}' not found.")

        # Clear entry fields
        self.entry_grade_id.delete(0, tk.END)
        self.entry_course.delete(0, tk.END)
        self.entry_grade.delete(0, tk.END)

    def view_grades(self):
        """
        View all grades for a specified student.
        """
        student_id = self.entry_view_grades_id.get().strip()

        if not student_id:
            messagebox.showerror("Input Error", "Student ID is required.")
            self.status_var.set("Failed to view grades: Student ID not provided.")
            return

        student = self.hash_table.retrieve(student_id)

        self.text_grades.delete('1.0', tk.END)

        if student:
            grades = student.grades
            if grades:
                grades_info = "\n".join([f"{course}: {grade}" for course, grade in grades.items()])
                info = (
                    f"Student ID: {student.student_id}\n"
                    f"Name: {student.name}\n"
                    f"Gender: {student.gender}\n"
                    f"Age: {student.age}\n"
                    f"Grades:\n{grades_info}\n"
                    f"Total Grades: {student.total_grade()}\n"
                    f"{'-'*40}\n"
                )
            else:
                info = (
                    f"Student ID: {student.student_id}\n"
                    f"Name: {student.name}\n"
                    f"No grades recorded.\n"
                    f"{'-'*40}\n"
                )
            self.text_grades.insert(tk.END, info)
            self.status_var.set(f"Viewed grades for student '{student.name}'.")
        else:
            self.text_grades.insert(tk.END, f"Student with ID '{student_id}' not found.")
            self.status_var.set(f"Failed to view student: ID '{student_id}' not found.")

    def create_display_tab(self):
        """
        Create the 'Display All Students' tab with a Treeview to show all student data.
        """
        frame = self.tab_display

        # Create a sub-frame for the display button
        button_frame = ttk.Frame(frame, padding="10")
        button_frame.pack(fill='x')

        # Display All Students Button
        btn_display = ttk.Button(button_frame, text="Display All Students", command=self.display_all_students, bootstyle='success-outline')
        btn_display.pack(side='right')
        ToolTip(btn_display, "Click to display all students in the system.")

        # Create a Treeview with Scrollbar
        tree_frame = ttk.Frame(frame, padding="10")
        tree_frame.pack(fill='both', expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical')
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Name", "Gender", "Age", "Grades", "Total"),
            show='headings',
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')

        # Define columns
        self.tree.heading("ID", text="Student ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Grades", text="Grades")
        self.tree.heading("Total", text="Total Grades")

        # Define column widths
        self.tree.column("ID", width=100, anchor='center')
        self.tree.column("Name", width=200, anchor='w')
        self.tree.column("Gender", width=100, anchor='center')
        self.tree.column("Age", width=50, anchor='center')
        self.tree.column("Grades", width=300, anchor='w')
        self.tree.column("Total", width=100, anchor='center')

        self.tree.pack(fill='both', expand=True)
        ToolTip(self.tree, "Displays all students with their details.")

    def display_all_students(self):
        """
        Display all students in the Treeview.
        """
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        for student in self.hash_table.get_all_students():
            grades_str = "; ".join([f"{course}: {grade}" for course, grade in student.grades.items()])
            self.tree.insert("", tk.END, values=(
                student.student_id,
                student.name,
                student.gender,
                student.age,
                grades_str,
                student.total_grade()
            ))
        self.status_var.set("Displayed all students.")

    def create_statistics_tab(self):
        """
        Create the 'Statistics' tab with options to view grade distributions and sort grades.
        """
        frame = self.tab_statistics

        # Create a sub-frame for statistics options
        stats_options_frame = ttk.Frame(frame, padding="20")
        stats_options_frame.pack(fill='x', expand=True)

        # Configure grid layout with appropriate padding
        stats_options_frame.columnconfigure(0, weight=1, pad=10)
        stats_options_frame.columnconfigure(1, weight=3, pad=10)
        stats_options_frame.columnconfigure(2, weight=1, pad=10)

        # Course Selection
        ttk.Label(stats_options_frame, text="Select Course:", font=('Helvetica', 10, 'bold')).grid(column=0, row=0, padx=5, pady=5, sticky='E')
        self.combo_course_stats = ttk.Combobox(stats_options_frame, values=self.get_all_courses(), state='readonly')
        self.combo_course_stats.grid(column=1, row=0, padx=5, pady=5, sticky='W')
        ToolTip(self.combo_course_stats, "Select the course for which you want to view statistics.")

        # Statistics Button
        btn_statistics = ttk.Button(stats_options_frame, text="Show Statistics", command=self.show_statistics, bootstyle='info-outline')
        btn_statistics.grid(column=2, row=0, padx=5, pady=5, sticky='W')
        ToolTip(btn_statistics, "Click to view statistics for the selected course.")

        # Sorting Options
        ttk.Label(stats_options_frame, text="Sort Grades:", font=('Helvetica', 10, 'bold')).grid(column=0, row=1, padx=5, pady=5, sticky='E')
        self.combo_sort_order = ttk.Combobox(stats_options_frame, values=["Ascending", "Descending"], state='readonly')
        self.combo_sort_order.grid(column=1, row=1, padx=5, pady=5, sticky='W')
        ToolTip(self.combo_sort_order, "Select the sort order for grades.")

        # Sort Grades Button
        btn_sort_grades = ttk.Button(stats_options_frame, text="Sort Grades", command=self.sort_grades_for_course, bootstyle='warning-outline')
        btn_sort_grades.grid(column=2, row=1, padx=5, pady=5, sticky='W')
        ToolTip(btn_sort_grades, "Click to sort grades for the selected course.")

        # Create a sub-frame for displaying statistics
        stats_display_frame = ttk.LabelFrame(frame, text="Grade Statistics", padding="20")
        stats_display_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Create a Text widget with Scrollbar to display statistics
        stats_text_frame = ttk.Frame(stats_display_frame)
        stats_text_frame.pack(fill='both', expand=True)

        scrollbar_stats = ttk.Scrollbar(stats_text_frame, orient='vertical')
        self.text_stats = tk.Text(stats_text_frame, width=100, height=15, yscrollcommand=scrollbar_stats.set, font=('Segoe UI', 10))
        scrollbar_stats.config(command=self.text_stats.yview)
        scrollbar_stats.pack(side='right', fill='y')
        self.text_stats.pack(side='left', fill='both', expand=True)
        ToolTip(self.text_stats, "Displays statistical analysis for the selected course.")

        # Create a sub-frame for displaying sorted grades
        sort_grades_display_frame = ttk.LabelFrame(frame, text="Sorted Grades", padding="20")
        sort_grades_display_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Create a Treeview with Scrollbar to display sorted grades
        sort_tree_frame = ttk.Frame(sort_grades_display_frame)
        sort_tree_frame.pack(fill='both', expand=True)

        scrollbar_sort = ttk.Scrollbar(sort_tree_frame, orient='vertical')
        self.tree_sort = ttk.Treeview(
            sort_tree_frame,
            columns=("Name", "Grade"),
            show='headings',
            yscrollcommand=scrollbar_sort.set
        )
        scrollbar_sort.config(command=self.tree_sort.yview)
        scrollbar_sort.pack(side='right', fill='y')

        # Define columns
        self.tree_sort.heading("Name", text="Name")
        self.tree_sort.heading("Grade", text="Grade")

        # Define column widths
        self.tree_sort.column("Name", width=300, anchor='w')
        self.tree_sort.column("Grade", width=100, anchor='center')

        self.tree_sort.pack(fill='both', expand=True)
        ToolTip(self.tree_sort, "Displays sorted grades for the selected course.")

    def get_all_courses(self):
        """
        Retrieve a sorted list of all courses from the hash table.

        Returns:
            list: Sorted list of course names.
        """
        courses = set()
        for student in self.hash_table.get_all_students():
            courses.update(student.grades.keys())
        return sorted(list(courses))

    def show_statistics(self):
        """
        Display statistical analysis for the selected course.
        """
        course = self.combo_course_stats.get().strip()

        if not course:
            messagebox.showerror("Input Error", "Please select a course for statistics.")
            self.status_var.set("Failed to show statistics: No course selected.")
            return

        students = []
        for student in self.hash_table.get_all_students():
            if course in student.grades:
                students.append(student)

        if not students:
            self.text_stats.delete('1.0', tk.END)
            self.text_stats.insert(tk.END, f"No grades found for course '{course}'.")
            self.status_var.set(f"Failed to show statistics: No grades for course '{course}'.")
            return

        stats = grade_statistics(students, course)

        self.text_stats.delete('1.0', tk.END)
        stats_info = f"Grade Statistics for '{course}':\n"
        stats_info += f"Average Grade: {stats['average']:.2f}\n"
        stats_info += f"Median Grade: {stats['median']}\n"
        stats_info += f"Mode Grade: {stats['mode']}\n\n"
        stats_info += "Grade Distribution:\n"
        for range_, count in stats['score_ranges'].items():
            stats_info += f"{range_}: {count} students\n"

        self.text_stats.insert(tk.END, stats_info)
        self.status_var.set(f"Displayed statistics for course '{course}'.")

    def sort_grades_for_course(self):
        """
        Sort and display grades for the selected course based on the chosen order.
        """
        course = self.combo_course_stats.get().strip()
        order = self.combo_sort_order.get().strip()

        if not course:
            messagebox.showerror("Input Error", "Please select a course for sorting.")
            self.status_var.set("Failed to sort grades: No course selected.")
            return

        if not order:
            messagebox.showerror("Input Error", "Please select a sort order (Ascending or Descending).")
            self.status_var.set("Failed to sort grades: No sort order selected.")
            return

        students = []
        for student in self.hash_table.get_all_students():
            if course in student.grades:
                students.append(student)

        if not students:
            messagebox.showinfo("No Data", f"No grades found for course '{course}'.")
            self.status_var.set(f"Failed to sort grades: No grades for course '{course}'.")
            return

        # Sort students based on grades
        sorted_students = sort_grades(students, course, order)

        # Clear existing data in the treeview
        for item in self.tree_sort.get_children():
            self.tree_sort.delete(item)

        # Insert sorted data
        for student in sorted_students:
            self.tree_sort.insert("", tk.END, values=(student.name, student.grades.get(course, 0)))

        self.status_var.set(f"Sorted grades for course '{course}' in {order} order.")

    def save_data_as(self):
        """
        Save data to a user-specified .txt or .csv file.
        """
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not file_path:
            self.status_var.set("Save operation canceled.")
            return
        try:
            save_to_file(self.hash_table, file_path)
            messagebox.showinfo("Saved", f"Data has been saved successfully to {file_path}.")
            self.status_var.set(f"Data saved successfully to {file_path}.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data.\n{e}")
            self.status_var.set(f"Failed to save data: {e}")

    def load_data_from(self):
        """
        Load data from a user-specified .txt or .csv file.
        """
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not file_path:
            self.status_var.set("Load operation canceled.")
            return
        progress = ttk.Progressbar(self.root, mode='indeterminate')
        progress.pack(side='top', fill='x')
        progress.start()
        try:
            load_from_file(self.hash_table, file_path)
            messagebox.showinfo("Loaded", f"Data has been loaded successfully from {file_path}.")
            self.display_all_students()
            self.status_var.set(f"Data loaded successfully from {file_path}.")
            # Update course combobox in statistics tab
            self.combo_course_stats['values'] = self.get_all_courses()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data.\n{e}")
            self.status_var.set(f"Failed to load data: {e}")
        finally:
            progress.stop()
            progress.destroy()

    def auto_save(self):
        """
        Automatically save data to the default .txt file at regular intervals.
        """
        try:
            # Define a default filename or choose based on your preference
            default_file = 'students.txt'  # Changed from 'students.json' to 'students.txt'
            save_to_file(self.hash_table, default_file)
            print("Auto-saved data.")
            self.status_var.set("Auto-saved data.")
        except Exception as e:
            print(f"Auto-save failed: {e}")
            self.status_var.set(f"Auto-save failed: {e}")
        finally:
            # Schedule the next auto-save
            self.root.after(300000, self.auto_save)  # 5 minutes

    def on_closing(self):
        """
        Handle the application closing event by prompting the user to save data.
        """
        try:
            if messagebox.askokcancel("Quit", "Do you want to save your changes before exiting?"):
                # Define a default filename or choose based on your preference
                default_file = 'students.txt'  # Changed from 'students.json' to 'students.txt'
                save_to_file(self.hash_table, default_file)
                self.status_var.set("Data saved. Exiting application.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving data: {e}")
            self.status_var.set(f"Error saving data: {e}")
        finally:
            self.root.destroy()

    def show_about(self):
        """
        Display information about the application.
        """
        about_text = (
            "Student Management System\n"
            "Version 2.3\n\n"
            "Developed by Jane Doe\n"
            "Email: jane.doe@example.com\n"
            "GitHub: github.com/janedoe\n\n"
            "This application allows you to manage student records efficiently, "
            "including adding, deleting, and retrieving student information, "
            "as well as managing grades and performing statistical analyses."
        )
        messagebox.showinfo("About", about_text)

    def change_theme(self, theme_name):
        """
        Change the application's theme.

        Args:
            theme_name (str): The name of the theme to apply.
        """
        self.style.theme_use(theme_name)
        self.status_var.set(f"Theme changed to '{theme_name}'.")
        # Update comboboxes if necessary
        self.update_course_combobox_stats()

    def update_course_combobox_stats(self):
        """
        Update the course selection combobox with the latest courses.
        """
        courses = self.get_all_courses()
        self.combo_course_stats['values'] = courses

def main():
    """
    Entry point of the Student Management Application.
    """
    # Initialize ttkbootstrap window with default theme
    root = ttk.Window(themename="superhero")
    app = StudentManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
