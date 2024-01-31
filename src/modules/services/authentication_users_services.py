from ..models.user import User
from ..models.role import Role
from ..repositories.users_repository import UsersRepository
from .password_services import PasswordServices
from fastapi import  HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..models.auth_response import AuthResponse
from ..services.user_validation_services import UserValidationServices
from ..services.token_services import TokenServices



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class AuthenticationUsersServices():
    _password_services=PasswordServices()
    _users_repository=UsersRepository()
    _auth_response=AuthResponse()
    _token_services= TokenServices()
    
    
    
    def authenticate_user(self, username:str, plain_password:str):
        user= UserValidationServices.check_user_validity(username)
        if user and self._password_services.verify_password(user.password, plain_password):
            return user
    
    
    def handle_authentication(self, username, plain_password):
        user=self.authenticate_user(username, plain_password)
        if not user:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},)
        
        access_token=self._token_services.create_access_token(user, user.role.scopes)
        refresh_token=self._token_services.create_refresh_token(user)
        return AuthResponse(access_token=access_token,refresh_token=refresh_token)
    
    def handle_refresh_access_token(self,user:User):
        access_token=self._token_services.create_access_token(user, user.role.scopes)
        return access_token
    
    


    
    

    

    
    
      
        
        