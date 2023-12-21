--4. Find the average grade on the stream (across the entire gradeboard).

SELECT  
    ROUND(AVG(grade), 2) AS average_grade
FROM
    grades;