from fastapi import APIRouter
from backend.models.categorymodel import CreateCategory, CreateTask,UpdateTask
from backend.crud.crud import create_category,get_category,get_all_categories,create_task,get_all_task_list,get_task_list_by_id, update_task,delete_task
from backend.db.database import task_collection

router = APIRouter()

@router.post("/category-create/")
def create_category_route(payload: CreateCategory):
    return create_category(payload)

@router.get("/category/{item_id}")
def get_category_route(item_id: str):
    return get_category(item_id)

@router.get("/categories")
def get_all_categories_route():
    return get_all_categories()

@router.post("/createtask/")
def create_task_route(payload: CreateTask):
    return create_task(payload)

@router.get("/get/task-list/{task_id}")
def get_task_list_by_id_route(task_id: str):
    return get_task_list_by_id(task_id)

@router.get("/get/task-list/")
def get_all_task_list_route():
    return get_all_task_list()

@router.put("/update-category/{category_id}")
async def update_category(category_id: str, payload: UpdateTask):
    return await update_task(category_id, payload)

@router.delete("/tasks/{task_id}")
async def delete_task_route(task_id: str):
    return delete_task(task_id)
