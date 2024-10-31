from sqlmodel import Field,Relationship, SQLModel
from typing import Optional
from datetime import datetime
from typing import Optional

class Subtask(SQLModel, table=True):
    __tablename__ = "subtasks"
    id:Optional[int]=Field(default=None, primary_key=True)
    subtask_name:str
    status:bool
    task_id:Optional[int]=Field(default=None, foreign_key="tasks.id")
    
    