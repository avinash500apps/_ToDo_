from fastapi import APIRouter,Request
from backend.crud.crud import create_document,get_document_by_id,get_all_documents,update_document,delete_document
from backend.models.model import User, CreateCategory, CreateTask, UpdateTask, Tasks, UpdateTasks,LoginRequest
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import Union
from fastapi import APIRouter, HTTPException, Depends
from backend.utils.utils import create_access_token,verify_password
from backend.db.database import users_collection


router = APIRouter()

# Get the absolute path to the templates folder
BASE_DIR = Path(__file__).resolve().parent.parent 
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/login")
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(payload: LoginRequest):
    user = users_collection.find_one({"email": payload.email})

    if not user or not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token = create_access_token(data={"email": user["email"]})
    return {"token": access_token, "message": "Login successful"}



@router.get("/sidebar")
def home(request: Request):
    return templates.TemplateResponse("sidebar.html", {"request": request})

@router.get("/popup")
def popup(request: Request):
    return templates.TemplateResponse("createtaskpopup.html", {"request": request})

@router.post("/create-document/{collection_name}")
async def create_item(
    collection_name: str, payload: Union[User, CreateCategory, CreateTask, Tasks, UpdateTasks]
):
    return create_document(collection_name, payload)

@router.get("/{collection_name}/{item_id}")
async def get_item(collection_name: str, item_id: str):
    return get_document_by_id(collection_name, item_id)


@router.get("/{collection_name}")
async def get_all_items(collection_name: str):
    return get_all_documents(collection_name)


@router.put("/update-document/{collection_name}/{item_id}")
async def update_item(collection_name: str, item_id: str, payload: dict):
    return update_document(collection_name, item_id, payload)


@router.delete("/delete-document/{collection_name}/{item_id}")
async def delete_item(collection_name: str, item_id: str):
    return delete_document(collection_name, item_id)
