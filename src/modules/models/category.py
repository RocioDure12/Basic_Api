from sqlmodel import Field,Relationship, SQLModel
from typing import Optional
from datetime import datetime
from typing import Optional

class Category(SQLModel, table=True):
    id:Optional[int]=Field(default=None, primary_key=True)
    category_name:str
    deleted_at:Optional[datetime] = None
    created_at:datetime = Field(default_factory=datetime.utcnow,nullable=False)
    updated_at:Optional[datetime] = None
    