from ..repositories.tasks_repository import TasksRepository
from ..models.task import Task
from typing import Annotated
from ..models.user import User
from fastapi import Security
from ..services.token_services import TokenServices

class TasksController:
    def __init__(self):
        self._tasks_repository=TasksRepository()
    
    def create(self,item:Task,user:Annotated[User,
                                               Security(TokenServices.check_access_token,
                                                        scopes=['tasks:create'])]):
        item.user_id=user.id
      
        return self._tasks_repository.create(item)

        
    def get_task_by_id(self,
                   user:Annotated[User,
                              Security(TokenServices.check_access_token,
                                           scopes=['tasks:get_task_by_id'])],
                   id):
        return self._tasks_repository.get_task_by_id(id)
    
    def read_my_tasks(self,user:Annotated[User,
                                               Security(TokenServices.check_access_token,
                                                        scopes=['tasks:read_my_tasks'])]):
        user_id=user.id
        return self._tasks_repository.read_my_tasks(user_id)
    
    
    
    def read_tasks_paginated(self):
        
        #return self._tasks_repository.read_my_tasks()
        count, items= self._tasks_repository.read_tasks_paginated(0, 2, '2025-04-30 10:39:00')
        return {
            "items":items,
            "total":count
        }
        
    def calculate_percentage_tasks_completed(self)->int:
        return self._tasks_repository.calculate_percentage_tasks_completed()
    
    def update(self,id,update_item:Task,user:Annotated[User,
                                               Security(TokenServices.check_access_token,
                                              scopes=['tasks:update'])]):
    
        return self._tasks_repository.update( id,update_item)
    
    def delete(self, id,user:Annotated[User,
                                       Security(TokenServices.check_access_token,
                                       scopes=['tasks:delete'])]):
        return self._tasks_repository.delete(id)
    
    def count_tasks(self,user:Annotated[User,
                                       Security(TokenServices.check_access_token,
                                       scopes=['tasks:count_tasks'])]):
        user_id=user.id
        
        return self._tasks_repository.count_tasks(user_id)
    
    def get_upcoming_tasks(self, user:Annotated[User,
                              Security(TokenServices.check_access_token,
                                           scopes=['tasks:get_upcoming_tasks'])]):
        user_id=user.id
        return self.get_upcoming_tasks() 