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