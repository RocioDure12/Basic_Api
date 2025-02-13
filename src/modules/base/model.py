from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel,Column,Date
from sqlalchemy import BigInteger,Integer
from abc import ABC, abstractmethod

# Modelo base con campos comunes para otras tablas

class BaseModel(SQLModel, table=False):
    id:Optional[int] = Field(sa_column=Column(Integer(), default=None, primary_key=True))
    deleted_at:Optional[datetime] = None
    created_at:Optional[datetime] = Field(default_factory=datetime.now,nullable=False)
    updated_at:Optional[datetime] = None