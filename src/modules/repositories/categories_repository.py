from typing import List, Type, Optional
from ..models.category import Category
from ..models.task import Task
from ..base.repository import BaseRepository
import os
from sqlmodel import select, func, Session
from dotenv import load_dotenv
load_dotenv()
from fastapi import HTTPException


class CategoriesRepository(BaseRepository[Category]):
    item:Type[Category]=Category
    max_categories=int(os.getenv('MAX_CATEGORIES'))
 
    
    def __init__(self):
        super().__init__()


    def create(self, item:Category)->Category:
        #current_count=self.count_categories(item.user_id)
        #if current_count >= self.max_categories:
         # //  raise ValueError("The maximum number of allowed categories has been reached.")
        with Session(self._db_services.get_engine()) as session:
            existing_category = session.exec(
                select(Category).where(
                    (Category.user_id == item.user_id) &
                    (Category.category_name == item.category_name)
                )
            ).first()

            if existing_category:
                raise HTTPException(
                    status_code=400,
                    detail=f"La categoría con nombre '{item.name}' ya existe para este usuario."
                )
        
            return super().create(item)
    
    
    def read_my_categories(self, user_id:int)->List[Category]:
        return super().get_items_by_user_id(user_id)
    

    def update(self, id, update_item)->Optional[Category]:
        return super().update(id, update_item)
    


    def delete(self, id: int) -> None:
        with Session(self._db_services.get_engine()) as session:
            category = session.exec(select(Category).where(Category.id == id)).one_or_none()

            if not category:
                raise HTTPException(status_code=404, detail="Categoría no encontrada.")

            tareas = session.exec(select(Task).where(Task.category_id == id, Task.deleted_at == None)).all()

            if tareas:
                # Error genérico, sin detalles
                raise HTTPException(
                    status_code=400,
                    detail="No se puede eliminar porque tiene tareas asociadas"
                )

            session.delete(category)
            session.commit()


#CORREGIR ESTE METODO PORQUE NO FUNCIONA BIEN
#
    def count_categories(self, user_id: int) -> int:
        with Session(self._db_services.get_engine()) as session:
            statement = select(func.count(Category.id)).where(Category.user_id == user_id)
            result= session.exec(statement)
            count=result.scalar()
        return count if count is not None else 0

                
            
        