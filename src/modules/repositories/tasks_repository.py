from ..services.db_services import DbServices
from sqlmodel import Date, Session, SQLModel, select
from ..models.task import Task
from ..models.user import User
from typing import List, Type
from ..base.repository import BaseRepository
from ..models.task import Task
import datetime
import time
from sqlalchemy import func


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
    

    def calculate_percentage_tasks_completed(self) -> int:
        today = datetime.date.today()

        with Session(self._db_services.get_engine()) as session:
            total_stmt = select(func.count()).select_from(self.item).where(
                func.date(self.item.due_date) == today
            )
            completed_stmt = select(func.count()).select_from(self.item).where(
                func.date(self.item.due_date) == today,
                self.item.status == True
            )

            total = session.exec(total_stmt).one()
            print(total)
            completed = session.exec(completed_stmt).one()
            print(completed)

        total_count = total
        completed_count = completed

        if total_count == 0:
            return 0

        return round((completed_count / total_count) * 100)

        
        
        


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


