"""
This module provides functions for interacting with the user and task data models using SQLAlchemy.

It includes functionality to create, read, update, and delete users and tasks in the database. 
Additionally, it implements user authentication and password hashing.

Functions:
- get_user_by_username: Retrieve a user by their username.
- get_user_by_user_id: Retrieve a user by their ID.
- get_all_users: Retrieve all users from the database.
- create_user: Create a new user in the database.
- update_user: Update an existing user in the database.
- delete_user: Delete a user from the database.
- authenticate_user: Authenticate a user by verifying their username and password.
- create_task: Create a new task for a user in the database.
- get_tasks_by_user: Retrieve all tasks for a specific user.
- get_task_by_id: Retrieve a specific task by its ID and owner ID.
- update_task: Update an existing task in the database.
- delete_task: Delete a specific task from the database.

Dependencies:
- SQLAlchemy: For database interactions.
- Passlib: For password hashing.
- Logging: For logging important events and errors.

Usage:
This module is intended to be used as part of a FastAPI application. It assumes an existing database setup
and defined User and Task models.
"""


from sqlalchemy.orm import Session
from .models import User, Task
from passlib.context import CryptContext
from logs.logger import logger
from typing import List, Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Retrieve a user from the database by their username.

    Args:
        db (Session): The database session.
        username (str): The username of the user.

    Returns:
        Optional[User]: The user object if found, otherwise None.
    """
    logger.info(f'Searching the database for the following username: {username}')
    return db.query(User).filter(User.username == username).first()

def get_user_by_user_id(db: Session, user_id: int) -> Optional[User]:
    """Retrieve a user from the database by their user ID.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user.

    Returns:
        Optional[User]: The user object if found, otherwise None.
    """
    logger.info(f'looking for the user with following in id in database: {user_id}')
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session) -> List[User]:
    """Retrieve all users from the database.

    Args:
        db (Session): The database session.

    Returns:
        List[User]: A list of user objects.
    """
    logger.info("Function was properly called")
    return db.query(User).all()

def create_user(db: Session, username: str, password: str, email: str) -> User:
    """Create a new user in the database.

    Args:
        db (Session): The database session.
        username (str): The username of the new user.
        password (str): The password for the new user.
        email (str): The email of the new user.

    Returns:
        User: The created user object.

    Raises:
        Exception: If there is an error during user creation.
    """
    hashed_password = pwd_context.hash(password)
    user = User(username=username, hashed_password=hashed_password, email=email)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f'user with data: {user} was saved')
        return user
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating user: {e}")
        raise e

def update_user(db: Session, user_id: int, email: str, username: str) -> Optional[User]:
    """Update an existing user in the database.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to update.
        email (str): The new email for the user.
        username (str): The new username for the user.

    Returns:
        Optional[User]: The updated user object if successful, otherwise None.
    """
    user = get_user_by_user_id(db, user_id=user_id)
    
    if user:
        user.username = username
        user.email = email
        db.commit()
        db.refresh(user)
        logger.info(f"Successfully updated the user: {username}")
        return user
    else:
        return None

def delete_user(db: Session, user_id: int) -> None:
    """Delete a user from the database.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to delete.

    Returns:
        None
    """
    user = get_user_by_user_id(db, user_id=user_id)
    
    if user:
        db.delete(user)
        db.commit()
        logger.info(f"user with following user_id: {user_id} was successfully deleted")
    else:
        return None

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Authenticate a user by verifying their username and password.

    Args:
        db (Session): The database session.
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        Optional[User]: The authenticated user object if successful, otherwise None.
    """
    user = get_user_by_username(db, username)
    if user and pwd_context.verify(password, user.hashed_password):
        return user
    return None

def create_task(db: Session, description: str, user_id: int) -> Task:
    """Create a new task for a user in the database.

    Args:
        db (Session): The database session.
        description (str): The description of the task.
        user_id (int): The ID of the user who owns the task.

    Returns:
        Task: The created task object.
    """
    task = Task(description=description, owner_id=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks_by_user(db: Session, user_id: int) -> List[Task]:
    """Retrieve all tasks for a specific user.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user.

    Returns:
        List[Task]: A list of task objects associated with the user.
    """
    return db.query(Task).filter(Task.owner_id == user_id).all()

def get_task_by_id(db: Session, owner_id: int, task_id: int) -> Optional[Task]:
    """Retrieve a specific task by its ID and owner ID.

    Args:
        db (Session): The database session.
        owner_id (int): The ID of the task owner.
        task_id (int): The ID of the task.

    Returns:
        Optional[Task]: The task object if found, otherwise None.
    """
    return db.query(Task).filter((Task.owner_id == owner_id) & (Task.id == task_id)).first() or []

def update_task(db: Session, owner_id: int, task_id: int, name: str, description: str, status: bool) -> Optional[Task]:
    """Update an existing task in the database.

    Args:
        db (Session): The database session.
        owner_id (int): The ID of the task owner.
        task_id (int): The ID of the task to update.
        name (str): The new name for the task.
        description (str): The new description for the task.
        status (bool): The new status of the task.

    Returns:
        Optional[Task]: The updated task object if successful, otherwise None.
    """
    task = db.query(Task).filter((Task.owner_id == owner_id) & (Task.id == task_id)).first() or []
    if task:
        task.name = name
        task.description = description
        task.status = status
        db.commit()
        db.refresh(task)
        return task
    else:
        return None

def delete_task(db: Session, owner_id: int, task_id: int) -> None:
    """Delete a specific task from the database.

    Args:
        db (Session): The database session.
        owner_id (int): The ID of the task owner.
        task_id (int): The ID of the task to delete.

    Returns:
        None
    """
    task = db.query(Task).filter((Task.owner_id == owner_id) & (Task.id == task_id)).first() or []

    if task:
        db.delete(task)
        db.commit()
        logger.info(f'task {task.description} was deleted successfully')
    else:
        return None
