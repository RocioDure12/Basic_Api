from ..services.db_services import DbServices
from sqlmodel import Session,select
from ..models.user import User
from typing import List
from ..services.password_services import PasswordServices
from sqlalchemy.orm import joinedload




class UsersRepository:
    def __init__(self):
        self._db_services=DbServices()
        self._password_services=PasswordServices()


    def get_by_verification_token(self, token:str):
        with Session(self._db_services.get_engine()) as session:
            statement=select(User).where(User.verification_code == token)
            result=session.exec(statement)
            user=result.one_or_none()
        return user
            
     
    def create(self, item:User):
        hashed_password=self._password_services.hash_password(item.password)
        item.password=hashed_password
        with Session(self._db_services.get_engine()) as session: 
            session.add(item)
            session.commit()
            session.refresh(item)
        return item
            
    
    def read(self)->list[User]:
        with Session(self._db_services.get_engine()) as session:
            statement = select(User)
            results=session.exec(statement)
            users=results.all()
        
        return users
    
    def read_by_username(self,username:str ):
        with Session(self._db_services.get_engine()) as session:
            # https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#sqlalchemy.orm.joinedload
            statement=select(User).where(User.username == username).options(joinedload(User.role))
            result=session.exec(statement)
            user=result.one_or_none()
        return user
    
    def read_by_id(self,id):
        with Session(self._db_services.get_engine()) as session:
            statement= select(User).where(User.id == id)
            result=session.exec(statement)
            user=result.one_or_none()
        return user        
        
    def update(self,id:int,update_item:User):
        
        with Session(self._db_services.get_engine()) as session:
            statement=select(User).where(User.id == id)
            result=session.exec(statement)
            user=result.one()
            
            if user:
                if update_item.password != user.password:
                    hashed_password=self._password_services.hash_password(update_item.password)
                    update_item.password=hashed_password
                    
            user.name=update_item.name
            user.surname=update_item.surname
            user.email=update_item.email
            user.username=update_item.username
            user.password=update_item.password
            user.disabled=update_item.disabled
            user.role_id=update_item.role_id
            session.add(user)
            session.commit()
            session.refresh(user)
            
        return user
                    
            
    def delete(self,id:int):
        with Session(self._db_services.get_engine()) as session:
            statement=select(User).where(User.id == id)
            result=session.exec(statement)
            user=result.one()
            session.delete(user)
            session.commit()
    
    """
    def pagination(self, skip:int=Query(0, alias="page"), limit:int=10, alias="element for page"):
        items=self.read()
        return items[skip:skip + limit]
    """    
    def read_users(self,offset:int, limit:int)->List[User]:
        with Session(self._db_services.get_engine()) as session:
            users = session.exec(select(User).offset(offset).limit(limit)).all()
            return users
        