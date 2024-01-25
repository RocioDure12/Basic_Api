from sqlmodel import Field,Relationship, SQLModel
from typing import Optional
from datetime import datetime
from typing import Optional


class Task(SQLModel, table=True):
    id:Optional[int]=Field(default=None, primary_key=True)
    task_name:str
    description:str
    status:bool
    deleted_at:Optional[datetime] = None
    created_at:datetime = Field(default_factory=datetime.utcnow,nullable=False)
    updated_at:Optional[datetime] = None
    date_time:datetime
    user_id:Optional[int]=Field(default=None, foreign_key="user.id")
  



