from pydantic import BaseModel, Field
from typing import List
from datetime import date, time

class CreateCategory(BaseModel):
    items: List[str]

class CreateTask(BaseModel):
    date: date 
    start_time: time
    end_time: time
    category: str = Field(..., min_length=1) 
    task_name: str = Field(..., min_length=1)
