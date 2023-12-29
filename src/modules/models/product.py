from sqlmodel import Field,Relationship, SQLModel
from typing import Optional, List
from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .category import Category
    from .user import User

class Product(SQLModel, table=True):
    id:Optional[int]=Field(default=None, primary_key=True)
    name:str
    deleted_at:Optional[datetime] = None
    created_at:datetime= Field(default_factory=datetime.utcnow,nullable=False)
    updated_at:Optional[datetime] = None
    category_id:Optional[int]=Field("category.id", nullable=False)
    category:Optional["Category"]=Relationship(back_populates="products")
    #user_id:Optional[int]=Field(foreign_key="user.id", nullable=False)
    #user:Optional["User"]=Relationship(back_populates="products")  