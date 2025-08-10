from typing import Optional, List
from sqlmodel import Field,Relationship, SQLModel
from pydantic import EmailStr
from datetime import datetime
from typing import TYPE_CHECKING
from ..models.role import Role
from ..models.task import Task
from ..base.model import BaseModel
from ..models.category import Category

class User(BaseModel,table=True):
    __tablename__ ="users"
    name:str
    surname:str
    email:str=Field(sa_column_kwargs={"unique": True})
    username:str=Field(sa_column_kwargs={"unique": True})
    password:str
    disabled:bool
    is_verified:bool
    verification_code:Optional[str]
    role_id:Optional[int]=Field(default=None, foreign_key="roles.id")
    role:Optional[Role]=Relationship()
    tasks:List[Task]=Relationship()
    categories:List[Category]=Relationship()

    

    
    