from typing import Optional, List
from sqlmodel import Field,Relationship, SQLModel
from pydantic import EmailStr
from datetime import datetime
from typing import TYPE_CHECKING
from ..models.role import Role
from ..models.task import Task

class User(SQLModel,table=True):
    __tablename__ ="users"
    id:Optional[int]=Field(default=None, primary_key=True)
    name:str
    surname:str
    email:str
    username:str
    password:str
    disabled:bool
    is_verified:bool
    verification_code:Optional[str]
    deleted_at:Optional[datetime]=None
    created_at:datetime=Field(default_factory=datetime.now,nullable=False)
    updated_at:Optional[datetime] = None
    role_id:Optional[int]=Field(default=None, foreign_key="role.id")
    role:Optional[Role]=Relationship()
    task:Optional[Task]=Relationship()
    

    
    