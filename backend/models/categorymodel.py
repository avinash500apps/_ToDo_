from pydantic import BaseModel, Field
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

class UpdateTask(BaseModel):
    date: Optional[datetime] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    category: Optional[str] = None
    task_name: Optional[str] = None


class Task(BaseModel):
    name: str
    age:int
    department:str
    salary:float
    due_date:datetime
    status: str = "New" 
    uid: str = None

class User(BaseModel):
    name: str
    email: str
    phone: str
