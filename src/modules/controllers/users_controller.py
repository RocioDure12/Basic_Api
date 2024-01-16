from ..models.user import User
from ..repositories.users_repository import UsersRepository
from fastapi.security import  OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import Depends, Security
from ..services.authentication_handler import AuthenticationHandler
from typing import List
from ..services.registration_handler import Registration_Handler



class UsersController():
    def __init__(self):
        self._users_repository=UsersRepository()
        self._authentication_handler=AuthenticationHandler()
        self._registration_handler=Registration_Handler
        
    def create(self, user:User):                 
        return self._registration_handler.handle_account_registration(user)

    
    
    def read(self, user:Annotated[User,
                                  Security(AuthenticationHandler.check_access_token,
                                           scopes=['users:read'])]):
        return self._users_repository.read()

    
    def read_by_id(self,
                   user:Annotated[User,
                              Security(AuthenticationHandler.check_access_token,
                                           scopes=['users:read_by_id'])],
                   id):
        return self._users_repository.read_by_id(id)
    
    def read_me(self, user:Annotated[User,
                                     Security(AuthenticationHandler.check_access_token,
                                              scopes=['users:read_me'])]):
        return user
    
    def update(self, id:int, update_item:Annotated[User,
                                     Security(AuthenticationHandler.check_access_token,
                                              scopes=['users: update'])]):
        
        return self._users_repository.update(id, update_item)
    
    def delete(self,id:int):
        return self._users_repository.delete(id)

    def login_user(self,form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        return self._authentication_handler.handle_authentication(form_data.username, form_data.password)
    
    def refresh_access_token(self,user:Annotated[User,
                                     Security(AuthenticationHandler.check_refresh_token)]):
       return self._authentication_handler.handle_refresh_access_token(user)
   

    def read_users(self, offset:int, limit:int):
        return self._users_repository.read_users(offset, limit)