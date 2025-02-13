from typing import List, Type, Optional
from ..models.category import Category
from ..base.repository import BaseRepository

class CategoriesRepository(BaseRepository[Category]):
    item:Type[Category]=Category
    
    def __init__(self):
        super().__init__()

    
    def create(self, item:Category)->Category:
        return super().create(item)
    
    def read_my_categories(self, user_id:int)->List[Category]:
        return super().get_items_by_user_id(user_id)
    
    def get_categories_count(self, id:int)->int:
        return super().get_total_items(id)
    
    def update(self, id, update_item)->Optional[Category]:
        return super().update(id, update_item)
    
    def delete(self, id)-> None:
        return super().delete(id)