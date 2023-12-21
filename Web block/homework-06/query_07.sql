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
    g.subject_id = 1; -- The subject for which you want to find the grades