from fastapi import APIRouter
from backend.models.categorymodel import User
from backend.crud.crud import create_user,get_user,update_user,delete_user

router = APIRouter()

@router.post("/users-create")
def create_user_route(payload: User):
    return create_user(payload)

@router.get("/get-user/{user_id}")
def get_user_route(user_id: str):
    return get_user(user_id)

@router.put("/update-user/{user_id}")
def update_user_route(user_id: str, user_data: User):
    return update_user(user_id, user_data)

@router.delete("/delete-user/{user_id}")
def delete_user_route(user_id: str):
    return delete_user(user_id)
