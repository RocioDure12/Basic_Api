from ..models.user import User
from ..repositories.users_repository import UsersRepository
from fastapi.security import  OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import Depends, Security
from ..services.authentication_users_services import AuthenticationUsersServices
from typing import List
#from ..services.registration_handler import Registration_Handler
from ..services.email_verification_services import EmailVerificationServices
from ..services.token_services import TokenServices



class UsersController():
    def __init__(self):
        self._users_repository=UsersRepository()
        self._authentication_users_services=AuthenticationUsersServices()
        self._email_verification_services=EmailVerificationServices()
        
        #self._registration_handler=Registration_Handler
        
    def create(self, user:User):                 
        #return self._registration_handler.handle_account_registration(user)
        return self._email_verification_services.handle_account_registration(user)
      

    
    
    def read(self, user:Annotated[User,
                                  Security(TokenServices.check_access_token,
                                           scopes=['users:read'])]):
        return self._users_repository.read()

    
    def read_by_id(self,
                   user:Annotated[User,
                              Security(TokenServices.check_access_token,
                                           scopes=['users:read_by_id'])],
                   id):
        return self._users_repository.read_by_id(id)
    
    def read_me(self, user:Annotated[User,
                                     Security(TokenServices.check_access_token,
                                              scopes=['users:read_me'])]):
        return user
    
    def update(self, id:int, update_item:Annotated[User,
                                     Security(TokenServices.check_access_token,
                                              scopes=['users: update'])]):
        
        return self._users_repository.update(id, update_item)
    
    def delete(self,id:int):
        return self._users_repository.delete(id)

    def login_user(self,form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        return self._authentication_users_services.handle_authentication(form_data.username, form_data.password)
    
    def refresh_access_token(self,user:Annotated[User,
                                     Security(TokenServices.check_refresh_token)]):
       return self._authentication_users_services.handle_refresh_access_token(user)
   

    def read_users(self, offset:int, limit:int):
        return self._users_repository.read_users(offset, limit)