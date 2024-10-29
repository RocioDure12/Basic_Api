from sqlmodel import Field,Relationship, SQLModel
from typing import Optional
from datetime import datetime
from typing import Optional
from ..models.category import Category
from ..models.subtask import Subtask
from ...base.model import BaseModel


class Task(BaseModel, table=True):
    __tablename__ ="tasks"
    task_name:str
    description:str
    status:bool=Field(default=False)
    due_date:datetime
    start_time: Optional[datetime] = Field(default=None)
    end_time: Optional[datetime] = Field(default=None) 
    user_id:Optional[int]=Field(default=None, foreign_key="user.id")
    category_id:Optional[int]=Field(default=None, foreign_key="category.id")
    
    category:Optional[Category]=Relationship()
    subtask:Optional[Subtask]=Relationship()
    

  



