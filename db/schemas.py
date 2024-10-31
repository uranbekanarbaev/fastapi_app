from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from enum import Enum

class StatusEnum(str, Enum):
    in_process = "in process"
    finished = "finished"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8)

class TaskCreate(BaseModel):
    title: str
    description: str
    status: StatusEnum

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True
        from_attributes=True