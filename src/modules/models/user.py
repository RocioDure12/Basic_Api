from typing import Optional, List
from sqlmodel import Field,Relationship, SQLModel
from pydantic import EmailStr
from datetime import datetime
from typing import TYPE_CHECKING
from ..models.role import Role
from ..models.task import Task
from ..base.model import BaseModel

class User(BaseModel,table=True):
    __tablename__ ="users"
    name:str
    surname:str
    email:str
    username:str
    password:str
    disabled:bool
    is_verified:bool
    verification_code:Optional[str]
    role_id:Optional[int]=Field(default=None, foreign_key="roles.id")
    role:Optional[Role]=Relationship()
    task:Optional[Task]=Relationship()
    

    
    