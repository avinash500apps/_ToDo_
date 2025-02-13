from backend.db.database import users_collection, category_collection,task_collection
from bson import ObjectId
from fastapi import HTTPException
from datetime import time
from pydantic import BaseModel
from backend.models.model import UpdateTask


COLLECTIONS = {
    "users": users_collection,
    "categories": category_collection,
    "tasks":task_collection
}

def time_to_str(t: time) -> str:
    return t.strftime("%H:%M:%S") if t else None

def create_document(collection_name: str, payload: BaseModel):
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")

    collection = COLLECTIONS[collection_name]
    document = payload.dict()

    if "start_time" in document:
        document["start_time"] = time_to_str(document["start_time"])
    if "end_time" in document:
        document["end_time"] = time_to_str(document["end_time"])

    try:
        result = collection.insert_one(document)
        document["_id"] = str(result.inserted_id)
        return {"message": f"{collection_name.capitalize()} created successfully", "data": document}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_document_by_id(collection_name: str, item_id: str):
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")

    collection = COLLECTIONS[collection_name]

    try:
        item = collection.find_one({"_id": ObjectId(item_id)})
        if not item:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} not found")
        item["_id"] = str(item["_id"])
        return {"message": f"{collection_name.capitalize()} retrieved successfully", "data": item}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



def get_all_documents(collection_name: str):
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")

    collection = COLLECTIONS[collection_name]

    try:
        documents = list(collection.find({}))
        if not documents:
            raise HTTPException(status_code=404, detail=f"No {collection_name} found")
        for doc in documents:
            doc["_id"] = str(doc["_id"])
        return {"message": f"{collection_name.capitalize()} retrieved successfully", "data": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_document(collection_name: str, item_id: str, payload: dict):
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")

    collection = COLLECTIONS[collection_name]

    update_data = payload
    print("update-data",update_data)

    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields provided for update")

    try:
        # Attempt the update operation
        update_result = collection.update_one({"_id": ObjectId(item_id)}, {"$set": update_data})

        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} not found")

        return {"message": f"{collection_name.capitalize()} updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_document(collection_name: str, item_id: str):
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")

    collection = COLLECTIONS[collection_name]

    try:
        result = collection.delete_one({"_id": ObjectId(item_id)})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} not found")

        return {"message": f"{collection_name.capitalize()} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
