from ..services.db_services import DbServices
from sqlmodel import Session, SQLModel,select
from ..models.task import Task
from ..models.user import User
from typing import List




class TasksRepository:
    def __init__(self):
        self._db_services = DbServices()
    
    def create(self, item:Task):
      
        with Session(self._db_services.get_engine()) as session:
            session.add(item)
            session.commit()
            session.refresh(item)
        return item
    
    def read_my_tasks(self, user_id)->[Task]:
        with Session(self._db_services.get_engine()) as session:
            statement=select(Task).where(Task.user_id == user_id)
            results=session.exec(statement)
            tasks=results.all()
        return tasks
        
    #pendiente de programar la logica de esta funcion
    
    def update(self, id:int, update_item:Task):
        with Session(self._db_services.get_engine()) as session:
            statement=select(Task).where(Task.id == id)
            result=session.exec(statement)
            task=result.one()
            task.task_name=update_item.task_name
            task.description=update_item.description
            task.status=update_item.status
            session.add(task)
            session.commit()
            session.refresh(task)
            
        return task
    
    def delete(self,id:int):
        with Session(self._db_services.get_engine()) as session:
            statement=select(Task).where(Task.id == id)
            result=session.exec(statement)
            task=result.one()
            session.delete(task)
            session.commit()
            
    def read_tasks(self,offset:int, limit:int)->List[Task]:
        with Session(self._db_services.get_engine()) as session:
            tasks = session.exec(select(Task).offset(offset).limit(limit)).all()
            return tasks
            
        
        