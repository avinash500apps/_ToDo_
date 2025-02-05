from fastapi import FastAPI
from backend.routers import tasks,user_routers

app = FastAPI()
# Include user and task routes with prefixes
app.include_router(user_routers.router)
app.include_router(tasks.router)
