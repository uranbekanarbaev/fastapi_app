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

project/ │ ├── db/ # Database models │ ├── auth/ # user_jwt_token generation and authentication │ ├── router/ # API routes  ├── tests/ # Test cases │ ├── app.py # Application entry point │ └── ... │ ├── Dockerfile │ └── docker-compose.yml │ ├── .env # Environment variables | ├── loggs/ # logger configuration │ └── README.md # Project documentation

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

pip install -r requirements.txt


### API Endpoints

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


### TASK DESCRIPTION
Задание для разработчика Python Backend Developer на FastAPI/Django

Описание проекта:
Вам необходимо создать API-сервис для управления пользователями и задачами с использованием FastAPI/Django. Сервис должен предоставлять возможность создания, чтения, обновления и удаления (CRUD) пользователей и задач. Кроме того, необходимо реализовать аутентификацию и авторизацию пользователей, а также написать тесты для всех реализованных функций

Требования:

0. Модели данных:
   - Пользователь:
     - ID (целое число, автоинкремент)
     - Имя (строка)
     - Электронная почта (строка)
     - Пароль (строка)
   - Задача:
     - ID (целое число, автоинкремент)
     - Название (строка)
     - Описание (строка)
     - Статус (строка, возможные значения: "новая", "в процессе", "завершена")
     - Пользователь_ID (внешний ключ на модель Пользователь)

1. API Endpoint'ы:
   - Пользователи:
     - GET /users - Получить список всех пользователей
     - GET /users/{user_id} - Получить информацию о конкретном пользователе
     - POST /users - Создать нового пользователя
     - PUT /users/{user_id} - Обновить информацию о пользователе
     - DELETE /users/{user_id} - Удалить пользователя
   - Задачи:
     - GET /tasks - Получить список всех задач
     - GET /tasks/{task_id} - Получить информацию о конкретной задаче
     - POST /tasks - Создать новую задачу
     - PUT /tasks/{task_id} - Обновить информацию о задаче
     - DELETE /tasks/{task_id} - Удалить задачу

2. Аутентификация и авторизация:
   - Использовать JWT токены для аутентификации пользователей
   - Реализовать защиту маршрутов, чтобы только аутентифицированные пользователи могли создавать, обновлять и удалять задачи
   - Ограничить доступ к задачам только для их владельцев

3. Валидация:
   - Использовать Pydantic/DRF для валидации входных данных

4. База данных:
   - Использовать SQLAlchemy/ORM Django для работы с базой данных SQLite

5. Документация:
   - Автоматически сгенерированная документация API с использованием Swagger (доступна по адресу `/docs`)

6. Тестирование:
   - Написать тесты для всех реализованных функций, включая:
     - Тесты для проверки корректности работы CRUD операций для пользователей и задач
     - Тесты для проверки аутентификации и авторизации
     - Тесты для проверки валидации входных данных

7. Дополнительно (не обязательно!):
 - Docker
    - Создать Dockerfile для контейнеризации приложения
    - Создать docker-compose файл для простого развёртывания базы данных и приложения
    - Обеспечить возможность запуска тестов в контейнере

Рекомендуемые инструменты:
- FastAPI:
  - Pydantic для валидации данных
  - SQLAlchemy для работы с базой данных
  - FastAPI Users для управления аутентификацией
  - Pytest для написания тестов

- Django:
  - Django REST Framework (DRF) для создания API
  - Django ORM для работы с базой данных
  - Simple JWT для аутентификации
  - Django Test для написания тестов

Дополнительные требования:
- Код должен быть структурированным и хорошо документированным
- С выполненной репой прикладывать видео раскатки сервера и пример его работы
- Проект должен включать README файл с инструкциями по запуску и тестированию