### Homework 12

In this homework, we continue to refine our REST API application from homework 11.

Task:

     - implement the authentication mechanism in the application;
     - implement an authorization mechanism using JWT tokens so that all operations with contacts are performed only 
       by registered users;
     - the user has access only to his transactions with contacts;

General requirements:

     When registering, if a user already exists with such an email, the server will return an HTTP 409 Conflict error;
     The server hashes the password and does not store it openly in the database;
     In case of successful user registration, the server should return the HTTP response status 201 Created and the 
     new user's data;
     For all POST operations to create a new resource, the server returns a status of 201 Created;
     During the POST operation - user authentication, the server accepts a request with user data (email, password) 
     in the body of the request;
     If the user does not exist or the password does not match, an HTTP 401 Unauthorized error is returned;
     The authorization mechanism using JWT tokens is implemented by a pair of tokens: the access token access_token 
     and the update token refresh_token.

The authentication process, as well as updates, are performed in the Postman program, which is very convenient for 
this purpose.

To run the application, you must first start a Docker container with postgres and install the poetry virtual 
environment along with the necessary libraries.

Then you need to execute the following commands:

    - to create migrations:

        * alembic init migrations
        * alembic revision --autogenerate -m "add User and Role tables"
        * alembic upgrade head

    - to launch the application:

        * uvicorn main:app --host localhost --port 8000 --reload