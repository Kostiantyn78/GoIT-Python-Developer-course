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