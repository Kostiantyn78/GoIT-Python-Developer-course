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