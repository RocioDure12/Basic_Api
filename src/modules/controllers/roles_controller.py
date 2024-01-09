from ..models.role import Role
from ..repositories.roles_repository import RolesRepository
from fastapi.security import  OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import Depends, Security
from ..services.users_services import UsersServices

class RolesController():
    def __init__(self):
        self._roles_repository=RolesRepository()
        self._users_services=UsersServices()
        
    def create(self, item:Annotated[Role,
                                  Security(UsersServices.check_access_token,
                                           scopes=['roles:create'])]):
        return self._roles_repository.create(item)
    
    def read(self, item:Annotated[Role,
                                  Security(UsersServices.check_access_token,
                                           scopes=['users:read'])]):
        return self._roles_repository.read()
    
    
    def update(self, id:int, update_item:Annotated[Role,
                                  Security(UsersServices.check_access_token,
                                           scopes=['roles:update'])]):
        return self._roles_repository.update(id, update_item)
    
    def delete(self,id:int):
        return self._roles_repository.delete(id)