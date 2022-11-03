from flask import jsonify
from App.models import Student
#from App.database import db


# Creates a new student given their name, programme and faculty
# Commits the student to the database and returns the student
def create_student(name, programme, faculty):
    new_student = Student(name=name, programme=programme, faculty=faculty)
    new_student.add()
    new_student.commit()
    #db.session.add(new_student)
    #db.session.commit()
    return new_student


# Gets a student by their name
def get_students_by_name(name):
    return Student.query.filter_by(name=name).all()


# Gets a student by their id
def get_student(id):
    return Student.query.get(id)


# Gets all students in the database
def get_all_students():
    return Student.query.all()


# Gets all students in the database and returns them as a JSON object
def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    return [student.to_json() for student in students]


# Gets all reviews for a student given their id.
# Returns the reviews as a JSON object
def get_all_student_reviews(id):
    student = Student.query.get(id)
    if not student:
        return {"error": "student not found"}, 404
    return [review.to_json() for review in student.reviews], 200


# Updates a student given their id, name, programme and faculty
# If name, programme or faculty is None, it is not updated
def update_student(id, name=None, programme=None, faculty=None):
    student = Student.query.get(id)
    if student:
        if name:
            student.name = name
        if programme:
            student.programme = programme
        if faculty:
            student.faculty = faculty
        student.add()
        student.commit()
        #db.session.add(student)
        #db.session.commit()
        return student
    return None


# Deletes a student given their id
def delete_student(id):
    student = Student.query.get(id)
    if student:
        student.delete()
        student.commit()
        #db.session.delete(student)
        #db.session.commit()
        return True
    return False
