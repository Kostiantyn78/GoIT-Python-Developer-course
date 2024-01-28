## Homework 10

In the past homework, we scraped the site http://quotes.toscrape.com.

Now we need to independently implement an analogue of such a site on `Django`:

     We implemented the possibility of registering on the site and entering the site.
     Made it possible to add a new author to the site only for a registered user.
     Made it possible to add a new quote to the site with an indication of the author only for registered users.
     Migrated your existing MongoDB database to SQLite for your site using a custom script.
     Made it possible to go to each author's page without user authentication.
     All quotes are viewable without user authentication.
     Pagination has been added (these are the next and previous buttons on our website).

Console commands that we use in the project:

- to create a project:

  1. `django-admin startproject hw_project`

  # launch from folder `...\hw_project`

- to create applications inside the project:
  1. `python manage.py startapp quotes`
  2. `python manage.py startapp users`
- to start the server:
  1. `python manage.py runserver`
- for migration:
  1. `python manage.py makemigrations`
  2. `python manage.py migrate`
  3. `python -m utils.migration`
