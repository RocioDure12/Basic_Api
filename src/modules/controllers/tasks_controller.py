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
                                                        scopes=[])]):
        item.user_id=user.id
        return self._tasks_repository.create(item)
    
    def read_my_tasks(self,user:Annotated[User,
                                               Security(TokenServices.check_access_token,
                                                        scopes=[])]):
        user_id=user.id
        return self._tasks_repository.read_my_tasks(user_id)
    
    def update(self):
        return self._tasks_repository.update()
    
    def delete(self):
        return self._tasks_repository.delete()