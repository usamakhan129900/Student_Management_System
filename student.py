# student.py

class Student:
    def __init__(self, student_id, name, gender, age):
        self.student_id = student_id
        self.name = name
        self.gender = gender
        self.age = age
        self.grades = {}

    def add_grade(self, course, grade):
        self.grades[course] = grade

    def total_grade(self):
        return sum(self.grades.values())

    def to_dict(self):
        return {
            'student_id': self.student_id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'grades': self.grades
        }

    @classmethod
    def from_dict(cls, data):
        student = cls(
            student_id=data['student_id'],
            name=data['name'],
            gender=data['gender'],
            age=data['age']
        )
        student.grades = data.get('grades', {})
        return student
