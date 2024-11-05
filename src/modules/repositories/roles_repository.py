from ..services.db_services import DbServices
from sqlmodel import Session, SQLModel,select
from ..models.role import Role
from typing import Optional, Type, List
from ..base.repository import BaseRepository


class RolesRepository(BaseRepository[Role]):
    item:Type[Role]=Role
    
    def __init__(self):
        self._db_services=DbServices()
        super().__init__()
        
    def create(self, item:Role)->Role:
        return super().create(item)
  

    def read(self)->List[Role]:
        return super().read()
   
    
    def update(self,id:int,update_item:Role)->Optional[Role]:
        return super().update(id, update_item)
        

    def delete(self,id:int)->None:
        return super().delete(id)
      
            