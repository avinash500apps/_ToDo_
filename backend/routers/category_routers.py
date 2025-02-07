from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException
from fastapi import HTTPException
from backend.models.categorymodel import createcategory,CreateTask
from backend.db.database import category_collection
from bson import ObjectId

router = APIRouter()


@router.post("/category-create/")
def create_category(payload: createcategory):
    category_dict = payload.dict()
    try:
       
        result = category_collection.insert_one(category_dict)
        category_dict["_id"] = str(result.inserted_id) 
        return {"message": "Category created successfully", "category": category_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/category/{item_id}")
def get_category(item_id: str):
    try:
        item = category_collection.find_one({"_id": ObjectId(item_id)})
        if not item:
            raise HTTPException(status_code=404, detail="Category not found")
        
        item["_id"] = str(item["_id"])  # Convert ObjectId to string for JSON serialization
        return {"message": "Category retrieved successfully", "category": item}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories")
def get_all_categories():
    try:
        categories = list(category_collection.find({}))

        if not categories:
            raise HTTPException(status_code=404, detail="No categories found")

        # Convert ObjectId to string for JSON serialization
        for category in categories:
            category["_id"] = str(category["_id"])

        return {"message": "Categories retrieved successfully", "categories": categories}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/createtask/")
def create_task(payload : CreateTask):
    category_dict = payload.dict()
    try:
       
        result = category_collection.insert_one(category_dict)
        category_dict["_id"] = str(result.inserted_id) 
        return {"message": "Category created successfully", "category": category_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))