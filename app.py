"""
Main Application for User and Task Management API

This module sets up the FastAPI application for managing users and tasks.
It includes routers for handling user-related and task-related endpoints.

Routers:
    - router_users: Handles user registration, login, and user management functionalities.
    - router_tasks: Manages task creation, retrieval, updating, and deletion for authenticated users.

Usage:
    To run the application, use the following command:
        uvicorn main:app --reload

Where `main` is the name of this file (without the .py extension).

Example:
    Once the application is running, you can access the API at:
        http://127.0.0.1:8000

API Documentation:
    The automatically generated API documentation can be accessed at:
        - Swagger UI: http://127.0.0.1:8000/docs
        - ReDoc: http://127.0.0.1:8000/redoc
"""


from fastapi import FastAPI
from router.router_users import router as router_users
from router.router_tasks import router as router_tasks

app = FastAPI()

app.include_router(router_users)
app.include_router(router_tasks)