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