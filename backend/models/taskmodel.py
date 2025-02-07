from datetime import datetime
import uuid
from pydantic import BaseModel

class Task(BaseModel):
    name: str
    age:int
    department:str
    salary:float
    due_date:datetime
    status: str = "New" 
    uid: str = None