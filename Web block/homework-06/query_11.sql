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
