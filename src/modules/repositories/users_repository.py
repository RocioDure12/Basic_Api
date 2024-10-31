from ..services.db_services import DbServices
from sqlmodel import Session,select
from ..models.user import User
from typing import List, Type
from ..services.password_services import PasswordServices
from sqlalchemy.orm import joinedload
from ..base.repository import BaseRepository

class UsersRepository(BaseRepository[User]):
    item:Type[User]=User
    
    def __init__(self):

        self._password_services=PasswordServices()
        super().__init__()
    
    def get_by_verification_token(self, token:str):
        with Session(self._db_services.get_engine()) as session:
            statement=select(self.item).where(self.item.verification_code == token)
            result=session.exec(statement)
            user=result.one_or_none()
        return user
    
    def create_admin(self, item:User):
        hashed_password=self._password_services.hash_password(item.password)
        item.password=hashed_password
        item.role_id=1
        item.is_verified=True
        return super().create(item)
    
    def create_user(self, item:User):
            hashed_password=self._password_services.hash_password(item.password)
            item.password=hashed_password
            item.role_id=2
            return super().create(item)
        
    def read(self)->list[User]:
        return super().read()
    
    def read_by_id(self, id):
         return super().read_by_id(id)
     
    def read_by_username(self,username:str ):
        with Session(self._db_services.get_engine()) as session:
            # https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.joinedload
            statement=select(User).where(self.item.username == username).options(joinedload(self.item.role))
            result=session.exec(statement)
            user=result.one_or_none()
        return user
    
    def update(self, id, update_item):
         return super().update(id, update_item)
     
    def delete(self, id):
         return super().delete(id)
    
    def get_items_paginated(self, offset, limit):
         return super().get_items_paginated(offset, limit)
    
