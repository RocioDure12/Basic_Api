from sqlmodel import Field,Relationship, SQLModel
from sqlalchemy import JSON, Column
from typing import Optional, List

class Role(SQLModel,table=True):
    __tablename__ = "roles"
    id:Optional[int]=Field(default=None, primary_key=True)
    name:str
    scopes:List[str]= Field(default={}, sa_column=Column(JSON))
    is_admin:bool
    
    #Se usa arbitrary_types_allowed=True porque el campo
    # scopes está configurado para utilizar el tipo JSON de SQLAlchemy
    # que es un tipo arbitrario no nativo de Python, lo cual Pydantic no validaría sin esta configuración.
    
    class Config:
        arbitrary_types_allowed=True