from sqlalchemy.orm import Session
from .models import User, Task
from passlib.context import CryptContext
from loggs.logger import logger
from typing import List

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    logger.info(username)
    return db.query(User).filter(User.username == username).first()

def get_all_users(db: Session):
    logger.info("Function was properly called")
    return db.query(User).all()

def create_user(db: Session, username: str, password: str):
    hashed_password = pwd_context.hash(password)
    user = User(username=username, hashed_password=hashed_password)
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

def get_all_tasks(db: Session, owner_id: int) -> List[Task]:
    return db.query(Task).filter(Task.user_id == owner_id).all()
