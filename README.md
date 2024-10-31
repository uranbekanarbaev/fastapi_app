# User and Task Management API

## Overview

This project is a Python Backend Developer assignment focused on creating an API service for managing users and tasks using FastAPI/Django. The service supports CRUD operations for users and tasks, implements authentication and authorization, and includes automated testing for all functionalities.

## Table of Contents

- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Authentication and Authorization](#authentication-and-authorization)
- [Running the Application](#running-the-application)
- [Testing the Application](#testing-the-application)
- [Additional Information](#additional-information)
- [Contributing](#contributing)
- [License](#license)

## Technologies Used

- FastAPI
- SQLAlchemy (or Django ORM)
- Pydantic
- JWT for authentication
- Docker (optional)
- Pytest for testing

## Project Structure

project/ │ ├── app/ # Main application code │ ├── models/ # Database models │ ├── routers/ # API routes  ├── tests/ # Test cases │ ├── main.py # Application entry point │ └── ... │ ├── docker/ # Docker-related files (optional) │ ├── Dockerfile │ └── docker-compose.yml │ ├── .env # Environment variables └── README.md # Project documentation

## Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites

- Docker installed on your machine (if using Docker)
- Python 3.8 or higher
- pip (Python package installer)

### Clone the Repository

```bash
git clone https://github.com/uranbekanarbaev/fastapi_app.git
cd fastapi_app



## Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites

- Docker installed on your machine (if using Docker)
- Python 3.8 or higher
- pip (Python package installer)

### Clone the Repository

```bash
git clone https://github.com/uranbekanarbaev/fastapi_app.git
cd fastapi_app


API Endpoints
Users
GET /users: Retrieve a list of all users
GET /users/{user_id}: Retrieve information about a specific user
POST /users: Create a new user
PUT /users/{user_id}: Update user information
DELETE /users/{user_id}: Delete a user
Tasks
GET /tasks: Retrieve a list of all tasks
GET /tasks/{task_id}: Retrieve information about a specific task
POST /tasks: Create a new task
PUT /tasks/{task_id}: Update task information
DELETE /tasks/{task_id}: Delete a task
Authentication and Authorization
JWT tokens are used for user authentication.
Route protection ensures only authenticated users can create, update, and delete tasks.
Access to tasks is limited to their respective owners.
Running the Application
Build and Run Containers (if using Docker)

Use Docker Compose to build and start your application and the database:

bash
Copy code
docker-compose up --build
Access the Application

Open your browser and navigate to http://localhost:8000.

Check API Documentation

FastAPI provides an automatic interactive API documentation at http://localhost:8000/docs.

Testing the Application
To run the tests, follow these steps:

Run Tests

You can run your tests inside the Docker container by executing:

bash
Copy code
docker-compose run test
Or directly using:

bash
Copy code
pytest
View Test Results

The test results will be displayed in the terminal. Ensure that all tests pass before deploying.

Additional Information
Code Structure: The project is organized into folders to separate concerns, including models, routers, and tests.
Documentation: Each module and function is documented with docstrings for better understanding.
Server Deployment: Video demonstrations of server deployment and usage examples are included in the repository.
Contributing
Contributions are welcome! Please feel free to submit a pull request.

License
This project is licensed under the MIT License.