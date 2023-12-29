from sqlmodel import Field,Relationship, SQLModel
from typing import Optional, List
from datetime import datetime
from typing import TYPE_CHECKING

from .product import Product
if TYPE_CHECKING:
    from .user import User


class Category(SQLModel, table=True):
    id:Optional[int]=Field(default=None, primary_key=True)
    name:str
    deleted_at:Optional[datetime] = None
    created_at:datetime= Field(default_factory=datetime.utcnow,nullable=False)
    updated_at:Optional[datetime] = None
    products:List[Product]=Relationship(back_populates="category")
    #user_id:Optional[int]=Field(foreign_key="user.id", nullable=False)
    #user:Optional["User"]=Relationship(back_populates="categories")  