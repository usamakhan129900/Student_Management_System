# main.py

from hash_table import HashTable
from student import Student
from utils import save_to_file, load_from_file, sort_grades, grade_statistics

def main():
    ht = HashTable()
    load_from_file(ht)

    while True:
        print("\n--- Student Management System ---")
        print("1. Add Student")
        print("2. Delete Student")
        print("3. Retrieve Student")
        print("4. Add Grades")
        print("5. Display All Students")
        print("6. Sort Grades for a Course")
        print("7. Grade Statistics for a Course")
        print("8. Save and Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            student_id = input("Enter Student ID: ")
            name = input("Enter Name: ")
            gender = input("Enter Gender: ")
            try:
                age = int(input("Enter Age: "))
            except ValueError:
                print("Invalid age. Please enter a number.")
                continue
            student = Student(student_id, name, gender, age)
            ht.insert(name, student)
            print("Student added successfully.")

        elif choice == '2':
            name = input("Enter Name of the student to delete: ")
            if ht.delete(name):
                print("Student deleted successfully.")
            else:
                print("Student not found.")

        elif choice == '3':
            name = input("Enter Name of the student to retrieve: ")
            student = ht.retrieve(name)
            if student:
                print(student)
            else:
                print("Student not found.")

        elif choice == '4':
            name = input("Enter Student Name to add grades: ")
            student = ht.retrieve(name)
            if student:
                while True:
                    course = input("Enter Course Name (or 'done' to finish): ")
                    if course.lower() == 'done':
                        break
                    try:
                        grade = float(input(f"Enter grade for {course}: "))
                        student.add_grade(course, grade)
                        print(f"Grade for {course} added.")
                    except ValueError:
                        print("Invalid grade. Please enter a number.")
            else:
                print("Student not found.")

        elif choice == '5':
            ht.display()

        elif choice == '6':
            course = input("Enter Course Name to sort grades: ")
            students = []
            for bucket in ht.table:
                for key, student in bucket:
                    if course in student.grades:
                        students.append(student)
            if not students:
                print(f"No grades found for course '{course}'.")
                continue
            sorted_grades = sort_grades(students, course)
            print(f"Sorted grades for {course}: {sorted_grades}")

        elif choice == '7':
            course = input("Enter Course Name for statistics: ")
            students = []
            for bucket in ht.table:
                for key, student in bucket:
                    if course in student.grades:
                        students.append(student)
            if not students:
                print(f"No grades found for course '{course}'.")
                continue
            stats = grade_statistics(students, course)
            print(f"Grade Statistics for {course}:")
            for range_, count in stats.items():
                print(f"{range_}: {count} students")

        elif choice == '8':
            save_to_file(ht)
            print("Data saved. Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
