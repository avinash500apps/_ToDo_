# backend/crud/curd.py
from backend.db.database import users_collection, category_collection
from bson import ObjectId
from backend.models.categorymodel import User,UpdateTask
from backend.models.categorymodel import CreateCategory, CreateTask
from fastapi import HTTPException
from pymongo.collection import Collection
from typing import Optional
from datetime import datetime, time, timezone

# Users CRUD Operations

def create_user(payload: User):
    user_dict = payload.dict()
    try:
        result = users_collection.insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id)
        return {"message": "User created successfully", "user": user_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_user(user_id: str):
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid user_id")

    if user:
        user["_id"] = str(user["_id"])
        return {"user": user}
    else:
        raise HTTPException(status_code=404, detail="User not found")

def update_user(user_id: str, user_data: User):
    try:
        user_id_obj = ObjectId(user_id)
        update_data = {}
        if user_data.name:
            update_data["name"] = user_data.name
        if user_data.email:
            update_data["email"] = user_data.email
        if user_data.phone:
            update_data['phone'] = user_data.phone

        users_collection.update_one({"_id": user_id_obj}, {"$set": update_data})
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid user_id or update data")

def delete_user(user_id: str):
    try:
        user_id_obj = ObjectId(user_id)
        result = users_collection.delete_one({"_id": user_id_obj})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid user_id")


# Categories CRUD Operations

def create_category(payload: CreateCategory):
    category_dict = payload.dict()
    try:
        result = category_collection.insert_one(category_dict)
        category_dict["_id"] = str(result.inserted_id)
        return {"message": "Category created successfully", "category": category_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_category(item_id: str):
    try:
        item = category_collection.find_one({"_id": ObjectId(item_id)})
        if not item:
            raise HTTPException(status_code=404, detail="Category not found")
        item["_id"] = str(item["_id"])  # Convert ObjectId to string for JSON serialization
        return {"message": "Category retrieved successfully", "category": item}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_all_categories():
    try:
        categories = list(category_collection.find({}))
        if not categories:
            raise HTTPException(status_code=404, detail="No categories found")
        for category in categories:
            category["_id"] = str(category["_id"])
        return {"message": "Categories retrieved successfully", "categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def create_task(payload: CreateTask):
    try:
        category_dict = payload.dict()
        category_dict["date"] = category_dict["date"].isoformat()
        category_dict["start_time"] = category_dict["start_time"].strftime("%H:%M:%S")
        category_dict["end_time"] = category_dict["end_time"].strftime("%H:%M:%S")

        result = category_collection.insert_one(category_dict)
        category_dict["_id"] = str(result.inserted_id)

        return {"message": "Task created successfully", "task": category_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_task_list_by_id(task_id: str):
    try:
        task = category_collection.find_one({"_id": ObjectId(task_id)})
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        task["_id"] = str(task["_id"])
        return {"task": task}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_all_task_list():
    try:
        tasks = list(category_collection.find({}))
        if not tasks:
            raise HTTPException(status_code=404, detail="No tasks found")
        for task in tasks:
            task["_id"] = str(task["_id"])
        return {"tasks": tasks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def time_to_str(t: Optional[time]) -> Optional[str]:
    return t.strftime("%H:%M:%S") if t else None
    

async def update_task(task_id: str, payload: UpdateTask):

    try:
        update_data = payload.dict()

        update_data = {key: value for key, value in update_data.items() if value is not None}

        if "date" in update_data:
            update_data["date"] = update_data["date"].isoformat()

        if "start_time" in update_data:
            update_data["start_time"] = update_data["start_time"].strftime("%H:%M:%S")

        if "end_time" in update_data:
            update_data["end_time"] = update_data["end_time"].strftime("%H:%M:%S")

        if "task_name" in update_data:
            task_name = update_data["task_name"]
            existing_task = category_collection.find({"task_name": task_name})
            if list(existing_task):
                raise HTTPException(400, "Task name already exists")

        task_data = category_collection.find_one({"_id": ObjectId(task_id)})

        if task_data:
            update_data["updated_at"] = datetime.now(timezone.utc)

            update_result = category_collection.update_one({"_id": ObjectId(task_id)}, {"$set": update_data})

            if update_result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Task not found")

            return {"message": "Task updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Task not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def delete_task(task_id: str):
    try:
        task_object_id = ObjectId(task_id)
        
        result = category_collection.delete_one({"_id": task_object_id})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")

        return {"message": "Task deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
