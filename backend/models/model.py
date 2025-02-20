from pydantic import BaseModel, Field, EmailStr
from typing import List
from datetime import datetime, time
from typing import Optional

class CreateCategory(BaseModel):
    items: List[str]

class CreateTask(BaseModel):
    date: datetime 
    start_time: time
    end_time: time
    category: str = Field(..., min_length=4) 
    task_name: str = Field(..., min_length=5)
    notes:str = Field(..., min_length=5)

class UpdateTask(BaseModel):
    date: Optional[datetime] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    category: Optional[str] = None
    task_name: Optional[str] = None
    notes: Optional[str] = None

class User(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name:str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Tasks(BaseModel):
    name:str

class UpdateTasks(BaseModel):
    name: Optional[str] = None