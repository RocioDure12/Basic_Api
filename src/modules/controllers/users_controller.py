from ..models.user import User
from ..repositories.users_repository import UsersRepository
from fastapi.security import  OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import Depends, Security
from ..services.users_services import UsersServices
from fastapi_pagination import Page, paginate,add_pagination


class UsersController():
    def __init__(self):
        self._users_repository=UsersRepository()
        self._users_services=UsersServices()
        
    def create(self, item:User):
        return self._users_repository.create(item)
    
    def read(self, user:Annotated[User,
                                  Security(UsersServices.check_access_token,
                                           scopes=['users:read'])]):
        return self._users_repository.read()
    
    def read_by_id(self,
                   user:Annotated[User,
                              Security(UsersServices.check_access_token,
                                           scopes=['users:read_by_id'])],
                   id):
        return self._users_repository.read_by_id(id)
    
    def read_me(self, user:Annotated[User,
                                     Security(UsersServices.check_access_token,
                                              scopes=['users:read_me'])]):
        return user
    
    def update(self, id:int, update_item:Annotated[User,
                                     Security(UsersServices.check_access_token,
                                              scopes=['users: update'])]):
        
        return self._users_repository.update(id, update_item)
    
    def delete(self,id:int):
        return self._users_repository.delete(id)

    def login_user(self,form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        return self._users_services.handle_authentication(form_data.username, form_data.password)
    
    def refresh_access_token(self,user:Annotated[User,
                                     Security(UsersServices.check_refresh_token)]):
       return self._users_services.handle_refresh_access_token(user)
   
    def get_users(self)->Page[User]:
        users=self._users_repository.read()
        return paginate(users)
        