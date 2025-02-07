from fastapi import APIRouter, HTTPException
from backend.db.database import users_collection
from backend.models.user_model import User
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/users-create")
def create_user(payload:User):
    user_dict = payload.dict()    
    try:
        result = users_collection.insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id) 
        return {"message": "User created successfully", "user": user_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/get-user/{user_id}")
def get_user(user_id: str):
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid user_id")
    
    if user:
        user_id = str(user.get("_id"))
        return {"user_id": user_id, "name": user.get("name"), "email": user.get("email")}
    else:
        raise HTTPException(status_code=404, detail="User not found")
    

@router.put("/update-user/{user_id}")
def update_user(user_id: str, user_data: User):
    try:
        user_id_obj = ObjectId(user_id)
       
        update_data = {}
        if user_data.name:
            update_data["name"] = user_data.name
        if user_data.email:
            update_data["email"] = user_data.email
        if user_data.phone:
            update_data['phone']=user_data.phone

        users_collection.update_one({"_id": user_id_obj}, {"$set": update_data})
        
        return {"message": "User updated successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid user_id or update data")

@router.delete("/delete-user/{user_id}")
def delete_user(user_id: str):
    try:
        user_id_obj = ObjectId(user_id)
        result = users_collection.delete_one({"_id": user_id_obj})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")

        return {"message": "User deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid user_id")
