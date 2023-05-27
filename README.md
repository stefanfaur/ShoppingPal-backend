# ShoppingPal Backend

This project is the backend for ShoppingPal, an application to help you manage your money better and keep track of your spending. It's built using FastAPI and relies on a PostgreSQL database for data persistence. This README will guide you through setting up and running the project locally.

# Table of Contents

1. [ShoppingPal Backend](#shoppingpal-backend)
2. [Prerequisites](#prerequisites)
3. [Getting Started](#getting-started)
4. [Project Structure](#project-structure)
5. [API Documentation](#api-documentation)
6. [Running Tests](#running-tests)
7. [Understanding the Docker Compose and Dockerfile](#understanding-the-docker-compose-and-dockerfile)
   * [docker-compose.yaml](#docker-compose.yaml)
   * [Dockerfile](#dockerfile)
8. [Project Dependencies](#project-dependencies)
9. [Running FastAPI without docker](#running-fastapi-without-docker)
   * [Step 1: Launch the Database Service](#step-1-launch-the-database-service)
   * [Step 2: Install Dependencies](#step-2-install-dependencies)
   * [Step 3: Launch the Application](#step-3-launch-the-application)
10. [The Database Data Model](#the-database-data-model)
11. [The API routes](#the-api-routes)
12. [Interacting with the database](#interacting-with-the-database)
	* [Code content](#code-content)
    * [Doing SQL queries on the database](#doing-sql-queries-on-the-database)
14. [Main module](#main-module)
15. [Tests](#tests)

## Prerequisites

Ensure you have the following software installed on your machine:

- Docker
- Docker-Compose

## Getting Started

Follow the steps below to clone the repository and run the project:

```bash
# clone the repo
git clone https://github.com/stefanfaur/ShoppingPal-backend.git

# navigate into the directory
cd ShoppingPal-backend

# use docker-compose to build and run the project
docker-compose up --build
# run with -d to run detached
```

## Project Structure

The project has the following structure:
```
tree-backend
├── api
│   ├── Dockerfile
│   ├── app
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── json_models.py
│   │   │   └── sql_models.py
│   │   ├── routers
│   │   │   ├── __init__.py
│   │   │   ├── get_receipt_items.py
│   │   │   ├── get_user_receipts.py
│   │   │   ├── submit.py
│   │   │   └── upload.py
│   │   ├── services
│   │   │   ├── __init__.py
│   │   │   ├── db_interaction.py
│   │   │   └── get_db.py
│   │   ├── test_image.jpg
│   │   └── test_main.py
│   ├── requirements.txt
│   └── test_api.sh
├── docker-compose.yml
└── init_db.sql
```

## API Documentation

The FastAPI project comes with auto-generated API documentation. After starting the project, open a web browser and navigate to [localhost:8000/docs](http://localhost:8000/docs) to access it.

## Running Tests
**At the moment tests need a new database to pass.
TODO: fix this.**
You can run tests by first entering the FastAPI container and then executing the script `test_api.sh`. Here's how you can do it:
```
# enter the fastapi container
docker exec -it shoppingpal-backend_fastapi_1 bash

# run the tests
bash test_api.sh
```
## Understanding the Docker Compose and Dockerfile

In this section, we will discuss what the `docker-compose.yaml` and `Dockerfile` do.

### docker-compose.yaml

`docker-compose.yaml` is a file used for defining and running multi-container Docker applications. It uses YAML syntax and each service defined will become a separate container when the command `docker-compose up` is run.

Here's what the provided docker-compose file does:

-   It specifies the version of Docker Compose file format (version 3.8 in this case).
    
-   It defines two services: `fastapi` and `receiptdb`.
    
    -   `fastapi`:
        -   The build context is set to the `api` directory, which means the `Dockerfile` located in that directory will be used for building the image.
        -   It is set to depend on `receiptdb`, which ensures `receiptdb` service starts before `fastapi`.
        -   Port `8000` of the host is mapped to port `80` of the `fastapi` container.
        -   The service is configured to always restart if it stops.
    -   `receiptdb`:
        -   The PostgreSQL image with version `15.3-alpine` is used.
        -   Similar to `fastapi`, this service will always restart if it stops.
        -   The environment variables `POSTGRES_USER` and `POSTGRES_PASSWORD` are set.
        -   Two volumes are mounted. The first one makes the data persist across container restarts and the second one is for initializing the database using the provided SQL script.
        -   Port `5432` of the host is mapped to port `5432` of the `receiptdb` container.

### Dockerfile

A `Dockerfile` is a script composed of various commands and arguments listed successively to automatically perform actions on a base image to create a new Docker image.

Here's what the provided Dockerfile does:

-   It sets the base image to `python:3.11`.
-   It sets the working directory in the container to `/code`.
-   It copies `requirements.txt`, `test_api.sh` and the `app` directory from your project to the `/code` directory in the Docker environment.
-   It installs the Python packages listed in `requirements.txt` using `pip`.
-   It exposes port `80` for the service within the Docker container.
-   The `CMD` command is used to provide defaults for executing the container. In this case, it will start the FastAPI application on port `80` using uvicorn.

# Project Dependencies

The ShoppingPal application is built using several Python libraries and modules. Docker takes care of the dependencies. 
 Here's a brief description of each of them:

1. **fastapi (0.95.2)**: This is the core web framework used in the application. It is known for its high performance and intuitive interface, and it makes the process of building APIs with Python easier.

2. **uvicorn (0.22.0)**: An ASGI server that allows your application to serve HTTP requests asynchronously, greatly increasing its performance. It is typically used to serve FastAPI applications.

3. **sqlalchemy (1.4.41)**: A powerful SQL toolkit and Object-Relational Mapping (ORM) system for Python, which makes it easier to interact with your database, in this case, PostgreSQL.

4. **psycopg2-binary (2.9.6)**: A PostgreSQL adapter for Python. It enables the application to connect with PostgreSQL database server.

5. **sqlmodel (0.0.8)**: An extension of SQLAlchemy and Pydantic, this package simplifies model definitions and operations for SQL databases.

6. **python-dotenv (1.0.0)**: A module that allows your application to read key-value pairs from a .env file and set them as environment variables.

7. **python-multipart (0.0.6)**: A module for parsing multipart/form-data requests, which are often used for file uploads. It is used here for handling receipt image uploads.

8. **requests (2.31.0)**: A popular Python library for making HTTP requests. It abstracts the complexities of making requests behind a beautiful, simple API.

9. **pytest (7.3.1)**: A robust testing framework for Python that simplifies the process of writing and running tests.

10. **httpx (0.24.1)**: A fully featured HTTP client for Python with similar interface to `requests`, but with additional features, like ability to make asynchronous requests.

These libraries and modules provide the backbone for the ShoppingPal application, offering functionalities that range from web request handling to database operations, file upload processing, and testing.

# Running FastAPI without docker

Follow these steps to get the ShoppingPal application up and running:

## Step 1: Launch the Database Service

We're using Docker to run the database service. To only launch the database service (named `receiptdb`), run the following command in your terminal:

bashCopy code

`docker-compose up -d receiptdb`

## Step 2: Install Dependencies

Next, we need to install all the Python dependencies for our application. We've listed these in the `requirements.txt` file. Run the following command to install them:

bashCopy code

`pip install -r requirements.txt`

## Step 3: Launch the Application

Finally, we can start our application.
**Make sure you edited the .env file accordingly**
We'll use Uvicorn, an ASGI server, to host our FastAPI application. The `--reload` option allows the server to restart whenever it detects a change in our code. The `--host 0.0.0.0` option makes our application accessible on all network interfaces of our machine. Here's the command to start the server:

bashCopy code

`uvicorn app.main:app --reload --host 0.0.0.0`

After running this command, you should be able to access the ShoppingPal application on your machine's local IP address, port 8000.

## The Database Data Model
The database consists of three tables: `User`, `Receipt`, and `Item`.

1.  **User**

The User table contains information about the user. It has the following columns:

-   `user_id`: The primary key for the user. This is a unique identifier for each user.
-   `is_admin`: A boolean indicating if the user is an admin. The default value is `False`.
-   `user_email`: The email address of the user.

The `User` table is linked to the `Receipt` table via a one-to-many relationship. One user can have many receipts, represented by the `receipts` field.

2.  **Receipt**

The Receipt table holds information about the receipt. It includes the following columns:

-   `id`: The primary key for the receipt.
-   `name`: The name of the receipt.
-   `shop_name`: The name of the shop where the receipt comes from.
-   `total`: The total amount of the receipt.
-   `date`: The date when the receipt was issued.
-   `user_id`: The foreign key linking to the `User` table.

There are two relationships in the `Receipt` table. It has a one-to-many relationship with the `Item` table, represented by the `items` field (one receipt can contain many items). Moreover, it is connected to the `User` table via the `user` field, creating a many-to-one relationship (many receipts can belong to one user).

3.  **Item**

The Item table includes information about items in the receipt. It has the following columns:

-   `id`: The primary key for the item.
-   `receipt_id`: The foreign key linking to the `Receipt` table.
-   `name`: The name of the item.
-   `count`: The quantity of the item.
-   `price`: The price of the item.

The `Item` table has a many-to-one relationship with the `Receipt` table. This means many items can belong to one receipt, represented by the `receipt` field.

These tables together form the schema of the database, allowing the recording of a user, their receipts, and the items in those receipts.

## The API routes
1.  `GET /receipts/{receipt_id}/items`:
    
    This endpoint is used to get the details of a receipt, including its associated items, based on a provided receipt ID. If the receipt ID does not exist in the database, it will return a 404 error with the message "Receipt not found". If it does exist, it will return the receipt along with its items. The `get_db` function is used to provide the database session.
    
2.  `GET /receipts/{user_id}`:
    
    This endpoint returns a list of all receipts associated with a particular user ID. If the user ID does not have any associated receipts or if the user does not exist, a 404 error with the message "Receipts not found" is returned. If the user ID exists and has associated receipts, those receipts are returned. The `get_db` function is used to provide the database session.
    
3.  `POST /save-receipt/`:
    
    This endpoint is used to save a new receipt. The receipt details are passed in the body of the POST request. A `user_id` is also provided (default is "1" for debugging purposes). The endpoint will then call `add_receipt` to save the receipt and iterate over the items in the receipt, calling `add_item_to_receipt` for each one to add them to the database. It returns a JSON response with the status of the operation. The `get_db` function is used to provide the database session.
    
4.  `POST /upload-image/`:
    
    This endpoint is used to upload an image of a receipt. The image file is passed in the body of the POST request. It then sends a POST request to an OCR (Optical Character Recognition) service to extract text from the image. If the OCR operation fails, it raises a 400 error with the message "OCR failed, check quota". The extracted details (merchant name, date, items, total) are then returned in a JSON format. The details are checked and formatted to handle potential errors (for instance, if some details are not recognized by the OCR service). This data can then be confirmed by the user in the frontend.
    
    5.  `GET /users/{user_id}`:
    
    This endpoint is used to retrieve a user based on the provided user ID. The `get_db` function is used to provide the database session. It queries the database for a user whose `user_id` matches the one given in the URL parameter. If the user is not found in the database, it raises a 404 error with the message "User not found". If the user is found, it returns the user's ID and admin status in a JSON format.
    
6.  `POST /users/`:
    
    This endpoint is used to create a new user. The user's details are passed in the body of the POST request in a JSON format (with the model `UserJ`). The `get_db` function is used to provide the database session. It then creates a new user record in the database with the provided details. The user's details are then committed to the database. The database session is refreshed to include the new user and this user object is returned in the response. This way, the user data returned in the response reflects the data that was actually stored in the database.
## Interacting with the database
### Code content
The backend interacts with the database using SQLAlchemy ORM (Object Relational Mapper) and SQLModel, which is a SQL ORM specifically designed for Python, built over SQLAlchemy and Pydantic.

Let's break down what each function does:

1.  `create_db_and_tables()`: This function is used to create all tables defined in SQLModel metadata, using the SQLAlchemy engine. This function is generally called at the beginning of the program, ensuring that all the necessary tables exist.
    
2.  `get_db()`: This is a generator function that creates a SQLAlchemy session, yields it (so it can be used elsewhere in the code), and then closes the session once it's no longer needed. It's designed this way to ensure that every database session is properly closed, which is a good practice for database management. This function is used with FastAPI's `Depends` function to provide a database session to each API endpoint function that needs one.
    
3.  `add_receipt()`: This function is used to create a new `Receipt` object and add it to the database. It takes the details of the receipt as arguments, creates a new `Receipt` object, and adds it to the session. The session is then committed (meaning that the new receipt is actually stored in the database), and the session is refreshed to reflect the new state of the database. The new `Receipt` object is then returned.
    
4.  `add_item_to_receipt()`: This function works similarly to `add_receipt()`, but it's used to add an `Item` to a particular `Receipt`. It takes the details of the item and the ID of the receipt to which it should be added as arguments. A new `Item` object is created and added to the session, which is then committed and refreshed.
    
5.  `get_user_receipts()`: This function is used to get all receipts for a particular user. It executes a SELECT statement on the `Receipt` table, filtering results by the `user_id` field. The result of this query is a collection of `Receipt` objects which is returned by the function.
    
6.  `get_receipt_with_items()`: This function is used to get a particular `Receipt` along with all its associated `Item` objects. It uses a SELECT statement with a joined load option, which means that it not only loads the `Receipt` but also all its related `Item` objects in a single query. This is more efficient than loading the `Receipt` and its `Item` objects in separate queries. The result is the `Receipt` object with its associated `Item` objects.
    

The backend also uses a `.env` file to securely store sensitive information such as the `DATABASE_URL`. This URL is loaded and passed to SQLAlchemy's `create_engine()` function to create the engine object that interacts with the database.
### Doing SQL queries on the database
We user pgAdmin4 to connect to the database and make queries for debugging purposes. 

## Main module
This main module sets up and starts the FastAPI application.

-   `FastAPI()` creates an instance of the FastAPI application.
-   `@app.on_event("startup")` is a FastAPI event handler that runs the `create_db_and_tables()` function when the application starts. This ensures the database and schema are created if they don't already exist.
-   `app.include_router()` is used multiple times to add various routers to the application, which define the API endpoints.
-   `app.add_middleware()` adds a middleware to the application, specifically a CORS (Cross-Origin Resource Sharing) middleware. This is used to control which origins (i.e., servers) are allowed to access the API. In this case, it allows the API to be accessed from `http://localhost:3000`.

## Tests
**Frameworks Used:**

1.  **Pytest**: A testing framework for Python that allows for simple unit testing as well as complex functional testing. Its capabilities can be enhanced with plugins. Here, it's used for creating test cases and fixtures.
    
2.  **FastAPI's TestClient**: A class provided by FastAPI that uses the `requests` library for making HTTP requests to the FastAPI application. This allows you to test your API routes in a way that mimics how they would be used in production.
    
3.  **SQLAlchemy**: A Python SQL toolkit and Object-Relational Mapping (ORM) system that provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access.
    

**Test Fixtures:**

-   `test_app`: Returns a TestClient instance that wraps the FastAPI application. This allows for making HTTP requests to the application within the test cases.
-   `db_cleanup`: This fixture uses SQLAlchemy to connect to the database, yielding a session for the tests to use, and then cleans up the database after each test.

**Test Cases:**

-   `test_upload_image`: This test case checks the `/upload-image/` endpoint. It opens a test image and posts it to the endpoint. The test passes if the HTTP status code is 200, indicating success.
    
-   `test_create_user`: Tests the `/users/` endpoint. It posts a new user to the endpoint and checks if the returned user_id matches the input and if the HTTP status code is 200.
    
-   `test_save_receipt`: Tests the `/save-receipt/` endpoint by posting a test receipt and checking if the response status is "success" and if the HTTP status code is 200.
    
-   `test_read_receipt_with_items`: Tests the `/receipts/1/items` endpoint by sending a GET request and checking if the returned receipt id is 1 and if the HTTP status code is 200.
    
-   `test_get_user`: Tests the `/users/new_user_id` endpoint by sending a GET request and checking if the returned user id matches the requested user id and if the HTTP status code is 200.
    
-   `test_read_user_receipts`: Tests the `/receipts/new_user_id` endpoint by sending a GET request and checking if the response is a list and if the HTTP status code is 200.
    

Overall, these tests ensure the API is functioning as expected by mimicking common requests and checking if the response matches the expected results.
