from ..services.db_services import DbServices
from sqlmodel import Session, SQLModel,select
from ..models.task import Task
from ..models.user import User
from typing import List, Type
from ..base.repository import BaseRepository
from ..models.task import Task


class TasksRepository(BaseRepository):
    item:Type[Task]=Task
    
    def __init__(self):
        super().__init__()
        
    def get_task_by_id(self,id:int):
        with Session(self._db_services.get_engine()) as session:
            statement=select(self.item).where(self.item.id == id)
            result=session.exec(statement)
            task=result.one_or_none()
        return task
            
            
    def create(self, item:Task):
        return super().create(item)
      

    def read_my_tasks(self, user_id)->List[Task]:
        return super().get_items_by_user_id(user_id)

    
    def update(self, id:int, update_item:Task):
        return super().update(id, update_item)
    
    def delete(self,id:int):
        return super().delete(id)
            
    def read_tasks_paginated(self,offset:int, limit:int)->List[Task]:
       return super().get_items_paginated(offset, limit)
        
        