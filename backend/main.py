from fastapi import FastAPI
from backend.routers import tasks,user_routers,category_routers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# Include user and task routes with prefixes
app.include_router(user_routers.router)
app.include_router(tasks.router)
app.include_router(category_routers.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
