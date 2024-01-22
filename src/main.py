from dotenv import load_dotenv
load_dotenv()
import os
from fastapi import FastAPI
from sqlmodel import Field, SQLModel, Session
from modules.routers.users_router import router as users_router
from modules.routers.roles_router import router as roles_router
from modules.models.user import User
from modules.services.db_services import DbServices


app = FastAPI()
app.include_router(users_router)
app.include_router(roles_router)
db=DbServices()



def create_tables():
    SQLModel.metadata.create_all(db.get_engine()) 

create_tables()



