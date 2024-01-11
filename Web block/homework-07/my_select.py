from sqlalchemy import func, desc, select, and_
from src.models import Student, Group, Teacher, Subject, Grade
from src.db import session


def select_1():
    """
        --1. Find the 5 students with the highest GPA across all subjects.

        SELECT
            st.id,
            st.fullname,
            ROUND(AVG(g.grade), 2) AS average_grade
        FROM
            students as st
        JOIN
            grades AS g ON st.id = g.student_id
        GROUP BY
            st.id
        ORDER BY
            average_grade DESC
        LIMIT 5;
            :return:
    """
    result = session.query(Student.id, Student.fullname,
                           func.round(func.avg(Grade.grade), 2).label('average_grade')).select_from(Student).join(
        Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()

    return result


def select_2():
    """
    --2. Find the student with the highest GPA in a particular subject.

    SELECT
        st.id,
        st.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM
        grades AS g
    JOIN
        students AS st ON st.id = g.student_id
    WHERE
        g.subject_id = 1 -- The subject in which you want to find the average grade
    GROUP BY
        st.id
    ORDER BY
        average_grade DESC
    LIMIT 1;
        :return:
    """
    result = session.query(Student.id, Student.fullname,
                           func.round(func.avg(Grade.grade), 2).label('average_grade')).select_from(Grade).join(
        Student).filter(Grade.subject_id == 1).group_by(Student.id).order_by(desc('average_grade')).limit(1).all()
    return result


def select_3():
    """
    --3. Find the average grade in groups for a certain subject.

    SELECT
        st.group_id,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM
        grades AS g
    JOIN
        students AS st ON st.id = g.student_id
    WHERE
        g.subject_id = 1 -- The subject in which you want to find the average grade
    GROUP BY
        st.group_id
    ORDER BY
        st.group_id;
    """

    result = session.query(Student.group_id, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Student).join(Grade).filter(Grade.subject_id == 1).group_by(Student.group_id) \
        .order_by(desc('average_grade')).all()
    return result


def select_4():
    """
    --4. Find the average grade on the stream (across the entire gradeboard).

    SELECT
        ROUND(AVG(grade), 2) AS average_grade
    FROM
        grades;
        :return:
    """

    result = session.query(func.round(func.avg(Grade.grade), 2).label('average_grade')).select_from(Grade).all()
    return result


def select_5():
    """
    --5. Find what courses a particular teacher teaches.

    SELECT
        t.fullname,
        sub.name
    FROM
        teachers AS t
    JOIN
        subjects AS sub ON t.id = sub.teacher_id
    WHERE
        t.id = 1; -- The teacher for which you want to find the subjects
    """

    result = session.query(Teacher.id, Teacher.fullname, Subject.id) \
        .select_from(Teacher).join(Subject, Teacher.id == Subject.teacher_id).filter(Subject.teacher_id == 1).all()
    return result


def select_6():
    """
    --6. Find a list of students in a specific group.

    SELECT
        fullname
    FROM
        students
    WHERE
        group_id = 1; -- The group for which you want to find the students
    """

    result = session.query(Student.id, Student.fullname).select_from(Student).join(Group).filter(Group.id == 1).all()
    return result


def select_7():
    """
    --7. Find the grades of students in a separate group for a specific subject.

    SELECT
        st.fullname,
        g.grade
    FROM
        students AS st
    JOIN
        grades AS g ON st.id = g.student_id
    WHERE
        st.group_id = 1 -- The group for which you want to find the students
     AND
        g.subject_id = 1; -- The subject for which you want to find the grades"""

    result = session.query(Student.id.label('student_id'), Student.fullname.label('student_name'), Grade.grade,
                           Grade.grade_date).select_from(Student).join(Grade, Student.id == Grade.student_id).join(
        Subject, Grade.subject_id == Subject.id).join(Group, Student.group_id == Group.id).filter(Group.id == 1,
                                                                                                  Subject.id == 2).all()
    return result


def select_8():
    """
    --8. Find the average grade given by a certain teacher in his subjects.

    SELECT
        t.fullname AS teacher,
        sub.name AS subject,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM
        teachers AS t
    JOIN
        subjects AS sub ON t.id = sub.teacher_id
    JOIN
        grades AS g ON sub.id = g.subject_id
    WHERE
        t.id = 1 -- The teacher for which you want to find the average grades
    GROUP BY
        t.fullname,
        sub.name;
    """
    result = session.query(Teacher.id, Teacher.fullname,
                           func.round(func.avg(Grade.grade), 2).label('average_grade')).select_from(Teacher).join(
        Subject, Subject.teacher_id == Teacher.id).join(Grade, Teacher.id == Grade.subject_id).filter(
        Teacher.id == 1).group_by(Teacher.id).all()
    return result


def select_9():
    """
    --9. Find a list of courses a student is taking.

    SELECT
        sub.name as courses
    FROM
        grades AS g
    JOIN
        subjects AS sub ON g.subject_id = sub.id
    WHERE
        g.student_id = 1 -- The student for which you want to find the courses
    GROUP BY
        sub.id;
    """

    result = session.query(Subject.name)\
        .select_from(Grade)\
        .join(Subject)\
        .filter(Grade.student_id == 1)\
        .group_by(Subject.id).all()
    return result


def select_10():
    """
    --10. A list of courses taught to a specific student by a specific teacher.

    SELECT
        sub.name AS subject
    FROM
        subjects AS sub
    JOIN
        grades AS g ON sub.id = g.subject_id
    WHERE
        sub.teacher_id = 1 -- The teacher for which you want to find the courses
     AND
        g.student_id = 1 -- The student for which you want to find the courses
    GROUP BY
        subject;
    """

    result = session.query(Subject.name)\
        .select_from(Grade).join(Subject)\
        .filter(and_(Subject.teacher_id == 1, Grade.student_id == 1))\
        .group_by(Subject.name).all()
    return result


def select_11():
    """
    --11. The average grade given by a particular teacher to a particular student.

    SELECT
        t.fullname AS teacher,
        st.fullname AS student,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM
        grades AS g
    JOIN
        students AS st ON st.id = g.student_id
    JOIN
        subjects AS sub ON sub.id = g.subject_id
    JOIN
        teachers AS t ON t.id = sub.teacher_id
    WHERE
        g.student_id = 1 -- The student for which you want to find the average grade
     AND
        t.id = 1 -- The teacher for which you want to find the average grade
    GROUP BY
        student,
        teacher;
    """

    result = session.query(Teacher.fullname, Student.fullname, func.round(func.avg(Grade.grade), 2)
        .label('average_grade'))\
        .select_from(Grade)\
        .join(Student)\
        .join(Subject)\
        .join(Teacher)\
        .filter(and_(Grade.student_id == 1, Teacher.id == 1))\
        .group_by(Student.fullname, Teacher.fullname).all()
    return result


def select_12():
    """
    --12. Grades of students in a certain group in a certain subject in the last lesson.

    SELECT
        st.fullname AS student,
        gr.name AS group_name,
        subj.name AS subject,
        m.grade as last_grade,
        MAX(m.date_of) AS last_date
    FROM
        students st
    JOIN
        grades m ON st.id = m.student_id
    JOIN
        subjects subj ON m.subject_id = subj.id
    JOIN
        groups gr ON st.group_id = gr.id
    WHERE
        gr.id = 1 -- The group for which you want to find the last grade
     AND
        subj.id = 1 -- The subject for which you want to find the last grade
    GROUP BY
        st.id, st.fullname
    ORDER BY
        st.id, last_date DESC;    """

    subquery = (select(func.max(Grade.grade_date)).join(Student, Grade.student_id == Student.id).filter(
        and_(Grade.subject_id == 1, Student.group_id == 1))).scalar_subquery()

    result = session.query(Student.id.label('student_id'), Student.fullname.label('student_fullname'),
                           Grade.grade, Grade.grade_date) \
        .select_from(Grade) \
        .join(Student) \
        .filter(and_(Grade.subject_id == 1, Student.group_id == 1, Grade.grade_date == subquery)) \
        .all()
    return result


if __name__ == '__main__':
    print(select_1())
    
    