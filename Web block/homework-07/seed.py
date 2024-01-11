from faker import Faker
from random import randint, choice

from sqlalchemy.exc import SQLAlchemyError

from src.db import session
from src.models import Student, Group, Teacher, Subject, Grade


fake = Faker('uk-Ua')

AMOUNT_STUDENTS = randint(30, 50)
AMOUNT_GROUPS = 3
AMOUNT_SUBJECTS = randint(5, 8)
AMOUNT_TEACHERS = randint(3, 5)
MAX_AMOUNT_MARKS = 20
AMOUNT_STUDENTS_PER_GROUP = int(AMOUNT_STUDENTS/AMOUNT_GROUPS)


def insert_groups():
    for _ in range(AMOUNT_GROUPS):
        group = Group(name=fake.word())
        session.add(group)
    session.commit()


def insert_students():
    for _ in range(AMOUNT_STUDENTS):
        student = Student(fullname=fake.name(), group_id=choice(session.query(Group.id).all())[0])
        session.add(student)
    session.commit()


def insert_teachers():
    for _ in range(AMOUNT_TEACHERS):
        teacher = Teacher(fullname=fake.name())
        session.add(teacher)
    session.commit()


def insert_subjects():
    for _ in range(AMOUNT_SUBJECTS):
        subject = Subject(name=fake.word(), teacher_id=choice(session.query(Teacher.id).all())[0])
        session.add(subject)
    session.commit()


def insert_grades():
    students = session.query(Student).all()
    subjects = session.query(Subject).all()
    for student in students:
        for subject in subjects:
            grade = Grade(
                grade=randint(1, 100),
                grade_date=fake.date_between(start_date='-30d', end_date='today'),
                student_id=student.id,
                subject_id=subject.id
            )
            session.add(grade)
    session.commit()


if __name__ == '__main__':
    try:
        insert_groups()
        insert_teachers()
        insert_students()
        insert_subjects()
        insert_grades()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()
