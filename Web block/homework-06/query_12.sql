--12. Grades of students in a certain group in a certain subject in the last lesson.

SELECT 
	st.fullname AS student,
	gr.name AS group_name,
	subj.name AS subject,
	m.grade as last_grade,
	MAX(m.date_of) AS last_date
FROM
    students st
JOIN
    grades m ON st.id = m.student_id
JOIN
    subjects subj ON m.subject_id = subj.id
JOIN
    groups gr ON st.group_id = gr.id
WHERE
    gr.id = 1 -- The group for which you want to find the last grade
 AND
    subj.id = 1 -- The subject for which you want to find the last grade
GROUP BY
    st.id, st.fullname
ORDER BY
    st.id, last_date DESC;