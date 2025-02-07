from pymongo import MongoClient

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")

# Database
db = client["MongodbPractice"]

# Collection
users_collection = db.get_collection("users")
task_collection= db.get_collection("tasks")
category_collection=db.get_collection("category")