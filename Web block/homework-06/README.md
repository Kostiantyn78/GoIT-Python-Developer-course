## Homework 06

We implemented a database, the scheme of which contains:

     Table of students;
     Table of groups;
     Table of teachers;
     Table of subjects with the indication of the teacher who reads the subject;
     A table where each student has grades in subjects with an indication of when the grade was received.

The resulting database was filled with random data (~30-50 students, 3 groups, 5-8 subjects, 3-5 teachers, up to 20 grades for each student in all subjects). We used the `Faker` package to fill the tables with the necessary data.

For each request, a separate file `query_number.sql` was issued, where instead of number, substitute the number of the request. We also created an additional file containing an `SQL` instruction that can be executed both in the database terminal and through the Pycharm `cursor.execute(sql).`
