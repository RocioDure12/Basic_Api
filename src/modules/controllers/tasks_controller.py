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
    
    def tasks_paginated(self,limit, offset,user:Annotated[User,
                                               Security(TokenServices.check_access_token,
                                              scopes=['tasks:tasks_paginated'])]):
        
        return self._tasks_repository.tasks_paginated(limit, offset)
    
    def update(self,id,update_item:Task,user:Annotated[User,
                                               Security(TokenServices.check_access_token,
                                              scopes=['tasks:update'])]):
    
        return self._tasks_repository.update( id,update_item)
    
    def delete(self, id,user:Annotated[User,
                                       Security(TokenServices.check_access_token,
                                       scopes=['tasks:delete'])]):
        return self._tasks_repository.delete(id)