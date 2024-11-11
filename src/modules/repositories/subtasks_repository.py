from ..base.repository import BaseRepository
from ..models.subtask import Subtask
from typing import List, Type, Optional,Annotated
from fastapi import Security
from ..services.token_services import TokenServices



class SubtaskRepository(BaseRepository[Subtask]):
    item:Type[Subtask]=Subtask
    
    def __init__(self):
        super().__init__()
        
    def create(self, item:Subtask)->Subtask:
        return super().create(item)
    
    def read_my_subtasks(self, user_id:int)->List[Subtask]:
        return super().get_items_by_user_id(user_id)
    
    def update(self, id, update_item)->Optional[Subtask]:
        return super().update(id, update_item)
    
    def delete(self, id)-> None:
        return super().delete(id)