from fastapi import FastAPI
from backend.routers import routers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(routers.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
