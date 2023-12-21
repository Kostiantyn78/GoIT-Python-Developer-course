--6. Find a list of students in a specific group.

SELECT
    fullname
FROM
    students
WHERE
    group_id = 1; -- The group for which you want to find the students