from fastapi.responses import JSONResponse
from pydantic import BaseModel
from backend.models.categorymodel import Task
from backend.db.database import task_collection
from fastapi import APIRouter, HTTPException
from datetime import datetime
import uuid
from fastapi import HTTPException
from bson import ObjectId
from pathlib import Path

router = APIRouter()
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

# Get the absolute path to the templates folder
BASE_DIR = Path(__file__).resolve().parent.parent  # This gets the 'backend' directory
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/")
def home(request: Request):
    names = ["Avinash", "Vinay", "Rakesh", "Kalyan"]

    data = {
        "request": request,
        "subject": "Welcome to Mantra!",
        "greeting": names,
        "message": "Thank you for joining Mantra. We are excited to have you onboard.",
        "sender_name": "Mantra Technologies"
    }
    return templates.TemplateResponse("sidebar.html", {"request": request})

@router.get("/popup")
def popup(request: Request):
    return templates.TemplateResponse("createtaskpopup.html", {"request": request})


@router.post("/task")
def create_tasks(payload: Task):
    
    if payload.uid is None:
        payload.uid = str(uuid.uuid4())
        print("After:", payload)

    task_data = payload.dict()
    
    try:
        task_collection.insert_one(task_data)
        return {"message": "Task created successfully"}
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create task")


@router.get("/get-task/{task_id}")
def get_task(task_id: str):
    try:
        task = task_collection.find_one({"_id": ObjectId(task_id)}) 
        
        if task:
           task_id = str(task.get("_id"))
           return {"task_id": task_id, "name": task.get("name"), "description": task.get("description")}
        else:
            raise HTTPException(status_code=404, detail="Task not found")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch task")
  
@router.put("/update-user/{task_id}")
def update_user(task_id: str, user_data: Task):
    try:
        user_id_obj = ObjectId(task_id)
        
        update_data = {}
        if user_data.name:
            update_data["name"] = user_data.name
        if user_data.age:
            update_data["age"] = user_data.age
        if user_data.department:
            update_data["department"] = user_data.department
        if user_data.salary:
            update_data["salary"] = user_data.salary
        if user_data.due_date:
            update_data["due_date"] = user_data.due_date
        if user_data.status:
            update_data["status"] = user_data.status
        if user_data.uid:
            update_data["uid"] = user_data.uid
        
        task_collection.update_one({"_id": user_id_obj}, {"$set": update_data})
        
        return {"message": "User updated successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid user_id or update data")
