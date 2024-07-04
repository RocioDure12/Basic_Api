from dotenv import load_dotenv
load_dotenv()
import os
from fastapi import FastAPI
from sqlmodel import Field, SQLModel, Session
from modules.routers.users_router import router as users_router
from modules.routers.roles_router import router as roles_router
from modules.routers.tasks_router import router as tasks_router
from modules.models.user import User
from modules.services.db_services import DbServices
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(users_router)
app.include_router(roles_router)
app.include_router(tasks_router)
db=DbServices()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_tables():
    SQLModel.metadata.create_all(db.get_engine()) 

#create_tables()


