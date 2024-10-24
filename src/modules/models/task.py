from sqlmodel import Field,Relationship, SQLModel
from typing import Optional
from datetime import datetime
from typing import Optional
from ..models.category import Category
from ..models.subtask import Subtask


class Task(SQLModel, table=True):
    __tablename__ ="tasks"
    id:Optional[int]=Field(default=None, primary_key=True)
    task_name:str
    description:str
    status:bool=Field(default=False)
    due_date:datetime
    deleted_at:Optional[datetime] = None
    created_at:datetime = Field(default_factory=datetime.now,nullable=False)
    updated_at:Optional[datetime] = None
    user_id:Optional[int]=Field(default=None, foreign_key="user.id")
    category_id:Optional[int]=Field(default=None, foreign_key="category.id")
    
    category:Optional[Category]=Relationship()
    subtask:Optional[Subtask]=Relationship()
    

  



