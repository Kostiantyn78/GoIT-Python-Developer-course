### Homework 13.1

In this homework, we continue to refine our REST API application from homework 12.

Task:

     - Implement a mechanism for verifying the registered user's e-mail;
     - Limit the number of requests to your contact routes. Be sure to limit the speed - creating contacts for the user;
     - Enable CORS for your REST API;
     - Implement the ability to update the user's avatar. Use the Cloudinary service;
     - Implement a caching mechanism using a Redis database. Cache the current user during authorization;
     - Implement a password reset mechanism for the REST API application.

General requirements:

     All environment variables must be stored in an .env file. There should be no confidential data in the "clean" form
     inside the code;
     Docker Compose is used to run all services and databases in the application.

The authentication process, as well as updates, are performed in the Postman program, which is very convenient for 
this purpose.

To run the application, you must first start a Docker Compose containers (`docker compose up -d`) with postgres, Redis
and install the poetry virtual environment along with the necessary libraries.

Then you need to execute the following commands:

    - to create migrations:

        * alembic init migrations
        * alembic revision --autogenerate -m "Init"
        * alembic upgrade head

    - to launch the application:

        * uvicorn main:app --host localhost --port 8000 --reload