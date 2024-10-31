from ..services.db_services import DbServices
from typing import Generic, TypeVar, List, Optional, Type
from abc import ABC
from sqlmodel import Session,select
from sqlalchemy.orm import joinedload

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    item: Type[T] 


    
    def __init__(self):
        self._db_services=DbServices()
    
    def create(self, item:T)-> T:
        with Session(self._db_services.get_engine()) as session: 
            session.add(item)
            session.commit()
            session.refresh(item)
        return item
    
    def read(self)-> List[T]:
        with Session(self._db_services.get_engine()) as session:
            statement = select(self.item)
            results=session.exec(statement)
            items=results.all()
        return items
    
    def read_by_id(self, id:int)-> Optional[T]:
        with Session(self._db_services.get_engine()) as session:
            statement= select(self.item).where(self.item.id == id)
            result=session.exec(statement)
            item=result.one_or_none()
        return item
        
    
    def update(self,id:int,update_item:T)-> Optional[T]:
        with Session(self._db_services.get_engine()) as session:
            statement=select(self.item).where(self.item.id == id)
            result=session.exec(statement)
            item=result.one_or_none()
            
            if item:
                for key, value in update_item.dict(exclude_unset=True).items():
                    setattr(item, key, value)
                    
                session.add(item)
                session.commit()
                session.refresh(item)
            return item
            
    
    def delete(self, id:int):
        with Session(self._db_services.get_engine()) as session:
            statement=select(self.item).where(self.item.id == id)
            result=session.exec(statement)
            item=result.one_or_none()
            if item:
                session.delete(item)
                session.commit()
        
    
    def get_items_paginated(self,offset:int, limit:int)->List[T]:
        with Session(self._db_services.get_engine()) as session:
            items = session.exec(select(self.item).offset(offset).limit(limit)).all()
            return items
        
    
    