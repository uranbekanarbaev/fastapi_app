"""
This module defines the API routes for managing tasks in the application.

It includes routes for:
- Retrieving all tasks for the current user.
- Retrieving a specific task by its ID.
- Creating a new task for the current user.
- Updating an existing task for the current user.
- Deleting a task for the current user.
- Authenticating a user and generating an access token.

Dependencies:
- FastAPI and its components for request handling, response generation, and dependency injection.
- SQLAlchemy for database interactions.
- Pydantic for data validation and serialization.
- Custom modules for database operations and JWT token generation.

Usage:
- The API routes are registered with the FastAPI application and can be accessed via HTTP methods (GET, POST, PUT, DELETE).
"""


from fastapi.routing import APIRouter
from fastapi import Request, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.exc import SQLAlchemyError

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from db.crud import (
    authenticate_user, get_tasks_by_user, create_task, get_task_by_id, update_task, delete_task
)
from auth.jwt_gen import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from db.database import get_db
from db.schemas import TaskCreate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from auth.user_auth import get_current_user
from db.models import User
from pathlib import Path
from logs.logger import logger

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")

def task_not_found(task):
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

@router.get("/tasks")
async def tasks(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retrieve all tasks for the current user.

    Args:
        request (Request): The incoming request.
        db (Session): The database session.
        current_user (User): The currently authenticated user.

    Returns:
        TemplateResponse: Renders the 'tasks.html' template with user tasks.
    """
    data = get_tasks_by_user(db, current_user.id)
    task_not_found(data)
    return templates.TemplateResponse(request, 'tasks.html', {"data": data})

@router.get("/tasks/{task_id}", response_class=HTMLResponse)
def get_task(request: Request, task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retrieve a specific task by its ID for the current user.

    Args:
        request (Request): The incoming request.
        task_id (int): The ID of the task to retrieve.
        db (Session): The database session.
        current_user (User): The currently authenticated user.

    Returns:
        TemplateResponse: Renders the 'tasks.html' template with the specific task.
    """
    data = get_task_by_id(db, current_user.id, task_id)
    task_not_found(data)
    return templates.TemplateResponse(request, 'tasks.html', {"data": data})

@router.post("/tasks")
def create_new_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create a new task for the current user.

    Args:
        task (TaskCreate): The task creation data.
        db (Session): The database session.
        current_user (User): The currently authenticated user.

    Returns:
        dict: A message indicating the success of task creation.
    """
    task = create_task(db, task.description, current_user.id)
    return {"task": task}

@router.put("/tasks/{task_id}")
def update_existing_task(task: TaskCreate, task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Update an existing task for the current user.

    Args:
        request (Request): The incoming request.
        task_id (int): The ID of the task to update.
        name (str): The new name of the task.
        description (str): The new description of the task.
        status (bool): The new status of the task.
        db (Session): The database session.
        current_user (User): The currently authenticated user.

    Returns:
        RedirectResponse: Redirects to the '/tasks' URL after updating the task.
    """
    task = update_task(db, current_user.id, task_id, task.title, task.description, task.status)
    task_not_found(task)
    return RedirectResponse(url='/tasks', status_code=303)

@router.delete("/tasks/{task_id}")
def delete_existing_task(request: Request, task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete a task for the current user.

    Args:
        request (Request): The incoming request.
        task_id (int): The ID of the task to delete.
        db (Session): The database session.
        current_user (User): The currently authenticated user.

    Returns:
        RedirectResponse: Redirects to the '/tasks' URL after deleting the task.
    """
    task = delete_task(db, current_user.id, task_id)
    task_not_found(task)
    return RedirectResponse(url='/tasks', status_code=303)

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate a user and return an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing username and password.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the access token and its type.

    Raises:
        HTTPException: If authentication fails due to incorrect username or password.
    """
    try:
        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            logger.warning(f"Authentication failed for username: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
