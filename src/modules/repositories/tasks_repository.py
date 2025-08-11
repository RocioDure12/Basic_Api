from ..services.db_services import DbServices
from sqlmodel import Session, SQLModel, select
from ..models.task import Task
from ..models.user import User
from typing import List, Type, Optional
from ..base.repository import BaseRepository
from sqlalchemy import func
from datetime import datetime, date, time
import time as time_module 


class TasksRepository(BaseRepository):
    item: Type[Task] = Task

    def __init__(self):
        super().__init__()

    def get_task_by_id(self, id: int):
        with Session(self._db_services.get_engine()) as session:
            statement = select(self.item).where(self.item.id == id)
            result = session.exec(statement)
            task = result.one_or_none()
        return task

    def create(self, item: Task):
        return super().create(item)

    def read_my_tasks(self, user_id) -> List[Task]:
        return super().get_items_by_user_id(user_id)

    def update(self, id: int, update_item: Task):
        return super().update(id, update_item)

    def delete(self, id: int):
        return super().delete(id)
    

    def count_tasks(self, user_id:int):
        return super().count_items(user_id)
    

    '''
    Utilizo métodos protegidos (los que empiezan con _) porque no se debería poder acceder
    a consultas sin ejecutar desde el controlador, sino solo dentro de la clase.
    '''
    def read_tasks_paginated(
            self,
            offset: int,
            limit: int,
            date: str
    ):
        with Session(self._db_services.get_engine()) as session:
            statement = super()\
                ._get_statement_paginated(offset, limit)\
                .where(self.item.due_date == date)    
            count = self._exec_count(statement)
            items = self._exec_select(statement)
            return count, items
        
        # return super().get_items_paginated(offset,limit)


    
        with Session(self._db_services.get_engine()) as session:
            statement = (
                select(self.item)
                .where(date(self.item.due_date) == date(date))
                .order_by(time(self.item.due_date))
                .offset(offset)
                .limit(limit)
            )
            tasks = session.exec(statement).scalars().all()

            count_statement = (
                select(statement.count())
                .select_from(self.item)
                .where(date(self.item.due_date) == date(date))
            )
            total = session.exec(count_statement).scalar()

        return {
            "items": [(task).dict() for task in tasks],
            "total": total
        }
    
    def get_upcoming_tasks(self, user_id:int,limit: int = 4,):
        with Session(self._db_services.get_engine()) as session:
            today = datetime.combine(datetime.today().date(), time.min)
            statement = (
                select(self.item)
                .where(
                    self.item.user_id == user_id,
                    self.item.due_date >= today
                )
                .order_by(self.item.due_date.asc())
                .limit(limit)
            )
            results = session.exec(statement).all()
            return results



    def get_task_dates_for_calendar(self, id:int):
        tasks=self.read_my_tasks(id)
        dates = {task.due_date for task in tasks if task.due_date}
        print(dates)

        return sorted(date.strftime('%Y-%m-%d') for date in dates)
    

    
    def get_tasks_by_user_and_date(self, user_id:int, offset:int, limit:int, date:Optional[date] = None):
        filters=[self.item.user_id == user_id]

        if date:
           
            filters.append(func.date(self.item.due_date) == date) # ✅ solo compara por fecha

        return self.get_items_paginated_with_total(offset, limit, filters)



    



