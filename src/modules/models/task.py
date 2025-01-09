from sqlmodel import Field,Relationship, SQLModel
from typing import Optional
from datetime import datetime, time,date
from typing import Optional
from ..models.category import Category
from ..models.subtask import Subtask
from ..base.model import BaseModel


class Task(BaseModel, table=True):
    __tablename__ ="tasks"
    task_name:str
    description:str
    status:bool=Field(default=False)
    due_date:date
    start_time: Optional[time] = Field(default=None)
    end_time: Optional[time] = Field(default=None) 
    user_id:Optional[int]=Field(default=None, foreign_key="users.id")
    category_id:Optional[int]=Field(default=None, foreign_key="categories.id")
    
    category:Optional[Category]=Relationship()
    subtask:Optional[Subtask]=Relationship()
    

  



