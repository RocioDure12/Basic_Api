from ..models.role import Role
from ..repositories.roles_repository import RolesRepository
from fastapi.security import  OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import Depends, Security
from ..services.authentication_users_services import AuthenticationUsersServices
from ..services.token_services import TokenServices
from ..models.user import User

class RolesController():
    def __init__(self):
        self._roles_repository=RolesRepository()
        self._authentication_handler=AuthenticationUsersServices()
        
    def create(self, item:Role, user:Annotated[User,
                                  Security(TokenServices.check_access_token,
                                           scopes=['roles:create'])]):
        return self._roles_repository.create(item)
    
    def read(self,user:Annotated[User,
                                  Security(TokenServices.check_access_token,
                                           scopes=['roles:read'])]):
        return self._roles_repository.read()
    
    
    def update(self, id:int, update_item:Role, user:Annotated[User,
                                  Security(TokenServices.check_access_token,
                                           scopes=['roles:update'])]):
        return self._roles_repository.update(id, update_item)
    
    def delete(self,id:int,user:Annotated[User,
                                  Security(TokenServices.check_access_token,
                                           scopes=['roles:delete'])]):
        return self._roles_repository.delete(id)