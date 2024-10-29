from ..modules.services.db_services import DbServices
from typing import Generic, TypeVar, List, Optional
from abc import ABC

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):

    
    def __init__(self):
        self._db_services=DbServices()
    
    def create(self, item:T)-> T:
        pass
    
    def read(self)-> List[T]:
        pass
    
    def read_by_id(self):
        pass
    
    def update(self):
        pass
    
    def delete(self):
        pass
    
    def get_items_paginated(self):
        pass
    
    