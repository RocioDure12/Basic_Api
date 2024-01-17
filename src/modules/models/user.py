from typing import Optional, List
from sqlmodel import Field,Relationship, SQLModel
from pydantic import EmailStr
from datetime import datetime
from typing import TYPE_CHECKING
from ..models.role import Role
#if TYPE_CHECKING:
#from .category import Category
#from .product import Product


class User(SQLModel,table=True):
    id:Optional[int]=Field(default=None, primary_key=True)
    name:str
    surname:str
    email:str
    username:str
    password:str
    disabled:bool
    is_verified:bool
    verification_code:str
    deleted_at:Optional[datetime]=None
    created_at:datetime=Field(default_factory=datetime.utcnow,nullable=False)
    updated_at:Optional[datetime] = None
    role_id:Optional[int]=Field(default=None, foreign_key="role.id")
    role:Optional[Role]=Relationship()
    
    #products:List[Product]=Relationship(back_populates="user")
    #categories:List[Category]=Relationship(back_populates="user")
    
    