from datetime import datetime, date, timedelta

from random import randint
import sqlite3

from faker import Faker

subjects = [
    "Вища математика",
    "Філософія",
    "Економіка підприємства",
    "Програмування",
    "Маркетинг",
    "Історія України",
    "Англійська",
    "Теорія імовірності"
]

groups = ['ПРБ-3', 'ЕП-1', 'ФК-1']
NUMBER_TEACHERS = randint(3, 5)
NUMBER_STUDENTS = randint(30, 80)
fake = Faker()
connect = sqlite3.connect('homework_DB.db')
cur = connect.cursor()


def seed_teachers():
    teachers = [fake.name() for _ in range(NUMBER_TEACHERS)]
    sql = "INSERT INTO teachers(fullname) VALUES(?);"
    cur.executemany(sql, zip(teachers,))


def seed_subjects():
    sql = "INSERT INTO subjects(name, teacher_id) VALUES(?, ?);"
    cur.executemany(sql, zip(subjects, iter(randint(1, NUMBER_TEACHERS) for _ in range(len(subjects)))))


def seed_groups():
    sql = "INSERT INTO groups(name) VALUES(?);"
    cur.executemany(sql, zip(groups,))


def seed_students():
    students = [fake.name() for _ in range(NUMBER_STUDENTS)]
    sql = "INSERT INTO students(fullname, group_id) VALUES(?, ?);"
    cur.executemany(sql, zip(students, iter(randint(1, len(groups)) for _ in range(len(students)))))


def seed_grades():
    start_date = datetime.strptime("2022-09-01", "%Y-%m-%d")
    end_date = datetime.strptime("2023-06-15", "%Y-%m-%d")
    sql = "INSERT INTO grades(subject_id, student_id, grade, date_of) VALUES(?, ?, ?, ?);"

    def get_list_date(start: date, end: date) -> list[date]:
        result = []
        current_date = start
        while current_date <= end:
            if current_date.isoweekday() < 6:
                result.append(current_date)
            current_date += timedelta(1)
        return result

    list_dates = get_list_date(start_date, end_date)

    grades = []
    for day in list_dates:
        random_subjects = randint(1, len(subjects))
        random_students = [randint(1, NUMBER_STUDENTS) for _ in range(5)]
        for student in random_students:
            grades.append((random_subjects, student, randint(1, 12), day.date()))
    cur.executemany(sql, grades)


if __name__ == '__main__':
    try:
        seed_teachers()
        seed_subjects()
        seed_groups()
        seed_students()
        seed_grades()
        connect.commit()
    except sqlite3.Error as error:
        print(error)
    finally:
        connect.close()
