from sqlalchemy.orm import Session
from .models import User, Task
from passlib.context import CryptContext
from loggs.logger import logger
from typing import List

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    logger.info(username)
    return db.query(User).filter(User.username == username).first()

def get_user_by_user_id(db: Session, user_id: int):
    logger.info(f'looking for the user with following {user_id}')
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session):
    logger.info("Function was properly called")
    return db.query(User).all()

def create_user(db: Session, username: str, password: str, email: str):
    hashed_password = pwd_context.hash(password)
    user = User(username=username, hashed_password=hashed_password, email=email)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f'user with data: {user} was saved')
        return user
    except Exception as e:
        db.rollback()  # Rollback to prevent partial commits
        logger.error(f"Error creating user: {e}")
        raise e  # Raise the exception for the calling function to handle
    
def update_user(db: Session, user_id: int, email: str, username: str):
    user = db.query(User).filter(User.id == user_id).first()
    
    if user:
        user.username = username
        user.email = email
        db.commit()
        db.refresh(user)
        logger.info(f"Successfully updated the user: {username}")
        return user
    else:
        return None
    
def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    
    if user:
        db.delete(user)
        db.commit()
        logger.info(f"user with following user_id: {user_id} was successfully deleted")
    else:
        return None

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if user and pwd_context.verify(password, user.hashed_password):
        return user
    return None

def create_task(db: Session, description: str, user_id: int):
    task = Task(description=description, owner_id=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks_by_user(db: Session, user_id: int):
    return db.query(Task).filter(Task.owner_id == user_id).all()

def get_task_by_id(db: Session, owner_id: int, task_id: int):
    return db.query(Task).filter((Task.owner_id == owner_id) & (Task.id == task_id)).first() or []

def update_task(db: Session, owner_id: int, task_id: int, name: str, description: str, status: bool):
    task = db.query(Task).filter((Task.owner_id == owner_id) & (Task.id == task_id)).first() or []
    if task:
        task.name = name
        task.description = description
        task.status = status
        db.commit()
        db.refresh(task)
    else:
        return None
    
def delete_task(db: Session, owner_id: int, task_id: int):
    task = db.query(Task).filter((Task.owner_id == owner_id) & (Task.id == task_id)).first() or []

    if task:
        db.delete(task)
        db.commit()
        logger.info(f'task {task.description} was deleted successfully')
    else:
        return None
