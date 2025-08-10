from sqlmodel import Session,select
from ..models.user import User
from typing import List, Type, Optional
from ..services.password_services import PasswordServices
from sqlalchemy.orm import joinedload
from ..base.repository import BaseRepository
from loguru import logger
import os
from fastapi import status
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv


load_dotenv()

class UsersRepository(BaseRepository[User]):
    item:Type[User]=User
    api_url = os.getenv("API_URL")
    
    def __init__(self):

        self._password_services=PasswordServices()
        super().__init__()
    
    def get_by_verification_token(self, token:str):
        with Session(self._db_services.get_engine()) as session:
            statement=select(self.item).where(self.item.verification_code == token)
            result=session.exec(statement)
            user=result.one_or_none()
        return user
    
    def create(self, item):
        logger.debug("Creating user")
        hashed_password=self._password_services.hash_password(item.password)
        item.password=hashed_password
        return super().create(item)
    
    def create_admin(self, item:User)->User:
        logger.debug("Creating admin user")
        item.role_id=1
        item.is_verified=True
        item.disabled=False
        return self.create(item)
    
    def create_user(self, item:User)->User:
            logger.debug("Creating user with role id 2")
            item.role_id=2
            return self.create(item)
        
    def read(self)->list[User]:
        return super().read()
    
    def read_by_id(self, id:int)->Optional[User]:
         return super().read_by_id(id)
     
    def read_by_username(self,username:str ) -> Optional[User]:
        with Session(self._db_services.get_engine()) as session:
            # https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.joinedload
            statement=select(User).where(self.item.username == username).options(joinedload(self.item.role))
            result=session.exec(statement)
            user=result.one_or_none()
        return user
    
    def update(self, id:int, update_item:User)-> Optional[User]:
         return super().update(id, update_item)
     
    def delete(self, id:int) ->None:
         return super().delete(id)
    
    def get_users_paginated(self, offset, limit)->List[User]:
         return super().get_items_paginated(offset, limit)
     
    def find_by_username_or_email(self, username: str, email: str) -> User | None:
        with Session(self._db_services.get_engine()) as session:
            statement = select(self.item).where(
                (self.item.username == username) | (self.item.email == email)
            )
            result = session.exec(statement)
            user = result.first()
            if user:
                # Aquí podés usar el usuario dentro del with, p.ej. cargar lazy relaciones si hace falta
                return user
            else:
                return None

