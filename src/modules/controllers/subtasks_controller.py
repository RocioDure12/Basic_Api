from ..repositories.subtasks_repository import SubtaskRepository
from ..models.subtask import Subtask
from typing import Annotated
from ..models.user import User
from fastapi import Security
from ..services.token_services import TokenServices

class SubtaskController():
    def __init__(self):
        self.subtasks_repository=SubtaskRepository()
        
    def create(self, item:Subtask, user:Annotated[User,
                                                          Security(TokenServices.check_access_token, 
                                                                   scopes=['subtasks:create'])]):
        return self.subtasks_repository.create(item)
    
    def read_my_subtasks(self,user_id:int, user:Annotated[User,
                                                          Security(TokenServices.check_access_token,
                                                                   scopes=['subtasks:read_my_subtasks'])]):
        return self.subtasks_repository.read_my_subtasks(user_id)
    
    def update(self, item_updated:Subtask, id:int,user:Annotated[User,
                                                          Security(TokenServices.check_access_token,
                                                                   scopes=['subtasks:update'])]):
        return self.subtasks_repository.update(id,item_updated)
    
    def delete(self, id:int,user:Annotated[User,
                                                          Security(TokenServices.check_access_token,
                                                                   scopes=['subtasks:delete'])]):
        return self.subtasks_repository.delete(id)