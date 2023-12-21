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