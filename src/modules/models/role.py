from sqlmodel import Field,Relationship, SQLModel
from sqlalchemy import JSON, Column
from typing import Optional, List

class Role(SQLModel,table=True):
    id:Optional[int]=Field(default=None, primary_key=True)
    name:str
    scopes:List[str]= Field(default={}, sa_column=Column(JSON))
    is_admin:bool
    
    class Config:
        arbitrary_types_allowed=True