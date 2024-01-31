## Homework 11

In this homework, we created a REST API to store and manage contacts. The API is built using the FastAPI infrastructure and uses SQLAlchemy for database management.

Contacts are stored in the database and contain the following information:

     Name
     Surname
     E-mail address
     Phone number
     Birthday
     Date of creation

The API has the ability to perform the following actions:

     Create a new contact
     Get a list of all contacts
     Get one contact per ID
     Update an existing contact
     Delete contact

In addition to the basic CRUD functionality, the API also has the following features:

     Contacts are available for search by name, surname or e-mail address (Query).
     The API should be able to retrieve a list of contacts with birthdays for the next 7 (or whatever) days.

General requirements:

     Using the FastAPI framework to create APIs
     Using ORM SQLAlchemy to work with the database
     PostgreSQL was used as a database.
     Support for CRUD operations for contacts
     Support for storing a contact's date of birth
     Provide API documentation
     Using the Pydantic data validation module

To run the application, you must first start a Docker container with postgres and install the poetry virtual 
environment along with the necessary libraries.

Then you need to execute the following commands:

    - to create migrations:

        * alembic init migrations
        * alembic revision --autogenerate -m 'Init'
        * alembic upgrade head

    - to launch the application:

        * uvicorn main:app --host localhost --port 8000 --reload