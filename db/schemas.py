"""
This module defines Pydantic models for user and task management in the application.

Models:
- StatusEnum: An enumeration representing the possible statuses of a task.
- UserCreate: A model for creating a new user, including validation for the user's name, 
  email, and password.
- TaskCreate: A model for creating a new task, including attributes for title, description, 
  and status.
- UserResponse: A model for representing a user's information in responses, providing the 
  user's ID, username, and email.

Usage:
These models are used for validating and serializing data in API requests and responses, 
ensuring that input data meets the required specifications and formats.
"""


from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from enum import Enum

class StatusEnum(str, Enum):
    """Enumeration for task status.

    Attributes:
        in_process (str): Represents a task that is currently in progress.
        finished (str): Represents a task that has been completed.
    """
    in_process = "in process"
    finished = "finished"

class UserCreate(BaseModel):
    """Model for creating a new user.

    Attributes:
        name (str): The name of the user.
        email (EmailStr): The email address of the user, validated as an email format.
        password (constr): The password for the user, must be at least 8 characters long.
    """
    username: str
    email: EmailStr
    password: constr(min_length=8)

class TaskCreate(BaseModel):
    """Model for creating a new task.

    Attributes:
        title (str): The title of the task.
        description (str): A detailed description of the task.
        status (StatusEnum): The current status of the task, using the StatusEnum.
    """
    title: constr(max_length=50)
    description: constr(max_length=500)
    status: StatusEnum

class UserResponse(BaseModel):
    """Model for representing a user response.

    Attributes:
        id (int): The unique identifier of the user.
        username (str): The username of the user.
        email (str): The email address of the user.

    Config:
        orm_mode (bool): Enables compatibility with ORM models.
        from_attributes (bool): Allows using attributes from the model for validation.
    """
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True
        from_attributes = True
