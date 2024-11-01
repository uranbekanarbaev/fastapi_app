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
    name: str
    email: EmailStr
    password: constr(min_length=8)

class TaskCreate(BaseModel):
    """Model for creating a new task.

    Attributes:
        title (str): The title of the task.
        description (str): A detailed description of the task.
        status (StatusEnum): The current status of the task, using the StatusEnum.
    """
    title: str
    description: str
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
