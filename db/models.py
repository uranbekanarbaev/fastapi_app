from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base, engine

class User(Base):
    """User model representing a user in the system.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The user's unique username.
        email (str): The user's unique email address.
        hashed_password (str): The hashed password for the user.
        tasks (list): The list of tasks associated with the user.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)

    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    """Task model representing a task assigned to a user.

    Attributes:
        id (int): The unique identifier for the task.
        name (str): The name of the task.
        description (str): A detailed description of the task.
        status (bool): The completion status of the task.
        owner_id (int): The identifier of the user who owns the task.
        owner (User): The user associated with the task.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(Boolean, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="tasks")

Base.metadata.create_all(bind=engine)
