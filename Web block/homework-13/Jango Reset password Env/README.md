## Homework 13.2

In this homework assignment, we modified the Django application from homework 10.

Task:

     Implement a password reset mechanism for a registered user;
     All environment variables must be stored in the `.env` file and used in the `settings.py` file.

Console commands that we use in the project (launch from folder `\hw_project\hw_project`):
- to create a project structure:
  - `python manage.py quotes`  
- to create applications inside the project:
  - `python manage.py startapp quotes` 
  - `python manage.py startapp users` 
- to start the server:
    - `python manage.py runserver`
- for migration:
    - `python manage.py makemigrations` 
    - `python manage.py migrate`
    - `python -m utils.migration`