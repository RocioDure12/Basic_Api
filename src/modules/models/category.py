from sqlmodel import Field,Relationship, SQLModel
from typing import Optional
from datetime import datetime
from typing import Optional
from ...base.model import BaseModel

class Category(BaseModel, table=True):
    __tablename__ ="categories"
    category_name:str
    user_id:Optional[int]=Field(default=None, foreign_key="user.id")
    
    