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
 