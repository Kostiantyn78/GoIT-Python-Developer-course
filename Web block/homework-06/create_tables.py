from psycopg2 import DatabaseError

from connection_to_DB import create_connection

# database table creation
def create_table(conn, create_table):
    try:
        c = conn.cursor()
        c.execute(create_table)
    except DatabaseError as err:
        print(err)


if __name__ == '__main__':
    # table for groups
    sql_create_groups = """
        DROP TABLE IF EXISTS [groups];
        CREATE TABLE [groups] (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name VARCHAR(50) UNIQUE
    );"""
    # table for students
    sql_create_students = """
        DROP TABLE IF EXISTS students;
        CREATE TABLE students (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        fullname STRING,
        group_id REFERENCES [groups] (id)
    );"""
    # table for teachers
    sql_create_teachers = """
        DROP TABLE IF EXISTS teachers;
        CREATE TABLE teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        fullname STRING
    );"""
    # table for subjects
    sql_create_subjects = """
        DROP TABLE IF EXISTS subjects;
        CREATE TABLE subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name STRING,
        teacher_id REFERENCES teachers (id)
    );"""
    # table for marks
    sql_create_grades = """
        DROP TABLE IF EXISTS grades;
        CREATE TABLE grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        subject_id REFERENCES subjects (id),
        student_id REFERENCES students (id),
        grade INTEGER,
        date_of DATE
    );"""

    with create_connection() as conn:
        if conn is not None:
            create_table(conn, sql_create_groups)
            create_table(conn, sql_create_students)
            create_table(conn, sql_create_teachers)
            create_table(conn, sql_create_subjects)
            create_table(conn, sql_create_grades)
        else:
            print("Error: can't create the database connection")
