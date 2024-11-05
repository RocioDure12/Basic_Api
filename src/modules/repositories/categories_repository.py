from typing import List, Type, Optional
from ..models.category import Category
from ..base.repository import BaseRepository

class CategoriesRepository(BaseRepository[Category]):
    item:Type[Category]=Category
    
    def __init__(self):
        super().__init__()
    
    def create(self, item):
        return super().create(item)
    
    def read_my_categories(self, user_id:int):
        return super().get_items_by_user_id(user_id)
    
    def update(self, id, update_item):
        return super().update(id, update_item)
    
    def delete(self, id):
        return super().delete(id)