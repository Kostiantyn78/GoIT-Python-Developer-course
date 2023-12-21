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