from typing import List, Type, Optional
from ..models.category import Category
from ..base.repository import BaseRepository
import os
from sqlmodel import select, func, Session
from dotenv import load_dotenv
load_dotenv()



class CategoriesRepository(BaseRepository[Category]):
    item:Type[Category]=Category
    #max_categories=int(os.getenv('MAX_CATEGORIES'))
    max_categories=15
    
    def __init__(self):
        super().__init__()


    def create(self, item:Category)->Category:
        current_count=self.count_categories(item.user_id)
        if current_count >= self.max_categories:
            raise ValueError("The maximum number of allowed categories has been reached.")
        
        return super().create(item)
    
    
    def read_my_categories(self, user_id:int)->List[Category]:
        return super().get_items_by_user_id(user_id)
    

    def update(self, id, update_item)->Optional[Category]:
        return super().update(id, update_item)
    
    def delete(self, id)-> None:
        return super().delete(id)


    def count_categories(self, user_id: int) -> int:
        with Session(self._db_services.get_engine()) as session:
            statement = select(func.count()).where(Category.user_id == user_id)
            return session.exec(statement).scalar_one()

                
            
        