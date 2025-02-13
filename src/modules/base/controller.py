from typing import Type, TypeVar,Generic
from abc import ABC
from repository import BaseRepository

T = TypeVar("T")
#Esta clase actua como un intermediario entre las vistas o (solicitudes del cliente)y los repositorios
class BaseController(ABC, Generic[T]):
    item: Type[T]
    
    def __init__(self):
        self.base_repository=BaseRepository()
    
    def create(self, item:T):
        return self.base_repository.create(item)
    
    def read(self):
        return self.base_repository.read()
    
    def read_by_id(self, id:int):
        return self.base_repository.read_by_id(id)  
      
    def update(self, id:int, updated_item):
        return self.base_repository.update(id, updated_item)
    
    def delete(self, id:int):
        return self.base_repository.delete(id)
    
    def get_items_paginated(self, offset:int, limit:int):
        return self.base_repository.get_items_paginated(offset, limit)
    
    def get_items_by_user_id(self, user_id:int):
        return self.base_repository.get_items_by_user_id(user_id)
    
    

        