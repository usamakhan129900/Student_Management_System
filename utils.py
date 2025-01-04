# utils.py

import os  # Ensure os is imported
import json
import csv
from hash_table import HashTable
from student import Student


def save_to_file(hash_table, file_path):
    """
    Save the hash table data to a CSV or TXT file.
    Each student's data is saved on a single line.

    Args:
        hash_table (HashTable): The hash table containing student data.
        file_path (str): The path to the file where data will be saved.
    """
    _, ext = os.path.splitext(file_path)
    if ext.lower() in ['.txt', '.csv']:
        # Determine delimiter based on extension
        delimiter = ',' if ext.lower() == '.csv' else '|'

        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=delimiter)
            # Write header
            writer.writerow(['Student ID', 'Name', 'Gender', 'Age', 'Grades'])

            for student in hash_table.get_all_students():
                grades_json = json.dumps(student.grades)  # Serialize grades as JSON string
                writer.writerow([student.student_id, student.name, student.gender, student.age, grades_json])
    else:
        raise ValueError("Unsupported file extension. Please use .txt or .csv.")


def load_from_file(hash_table, file_path=None):
    """
    Load data into the hash table from a CSV or TXT file.
    Each student's data should be on a single line.

    Args:
        hash_table (HashTable): The hash table where data will be loaded.
        file_path (str, optional): The path to the file from which data will be loaded.
                                   If None, it defaults to 'students.txt'.
    """
    if not file_path:
        file_path = 'students.txt'  # Default file

    _, ext = os.path.splitext(file_path)
    if ext.lower() in ['.txt', '.csv']:
        # Determine delimiter based on extension
        delimiter = ',' if ext.lower() == '.csv' else '|'

        if not os.path.exists(file_path):
            # If the file does not exist, initialize an empty hash table
            hash_table.clear()
            return

        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            hash_table.clear()
            for row in reader:
                student_id = row['Student ID']
                name = row['Name']
                gender = row['Gender']
                age = int(row['Age']) if row['Age'] else 0
                grades_json = row['Grades']
                grades = json.loads(grades_json) if grades_json else {}

                student = Student(student_id, name, gender, age)
                student.grades = grades
                hash_table.insert(student_id, student)
    else:
        raise ValueError("Unsupported file extension. Please use .txt or .csv.")


def sort_grades(students, course, order='Ascending'):
    """
    Sort students based on their grade in a specific course.

    Args:
        students (list): List of Student objects.
        course (str): The course name to sort by.
        order (str, optional): 'Ascending' or 'Descending'. Defaults to 'Ascending'.

    Returns:
        list: Sorted list of Student objects.
    """
    reverse = True if order == 'Descending' else False
    return sorted(students, key=lambda s: s.grades.get(course, 0), reverse=reverse)


def grade_statistics(students, course):
    """
    Calculate statistics for grades in a specific course.

    Args:
        students (list): List of Student objects.
        course (str): The course name to calculate statistics for.

    Returns:
        dict: A dictionary containing average, median, mode, and grade distribution.
    """
    grades = [s.grades[course] for s in students if course in s.grades]
    if not grades:
        return {}

    average = sum(grades) / len(grades)
    sorted_grades = sorted(grades)
    n = len(grades)
    median = sorted_grades[n // 2] if n % 2 != 0 else (sorted_grades[n // 2 - 1] + sorted_grades[n // 2]) / 2

    # Calculate mode
    frequency = {}
    for grade in grades:
        frequency[grade] = frequency.get(grade, 0) + 1
    mode = max(frequency, key=frequency.get)

    # Grade distribution
    score_ranges = {
        "90-100": 0,
        "80-89": 0,
        "70-79": 0,
        "60-69": 0,
        "Below 60": 0
    }

    for grade in grades:
        if 90 <= grade <= 100:
            score_ranges["90-100"] += 1
        elif 80 <= grade < 90:
            score_ranges["80-89"] += 1
        elif 70 <= grade < 80:
            score_ranges["70-79"] += 1
        elif 60 <= grade < 70:
            score_ranges["60-69"] += 1
        else:
            score_ranges["Below 60"] += 1

    return {
        'average': average,
        'median': median,
        'mode': mode,
        'score_ranges': score_ranges
    }
