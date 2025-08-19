from ..models.user import User
from ..models.role import Role
from ..repositories.users_repository import UsersRepository
from .password_services import PasswordServices
from fastapi import  HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer
from ..models.auth_response import AuthResponse
from ..services.user_validation_services import UserValidationServices
from ..services.token_services import TokenServices
from fastapi.responses import RedirectResponse
from ..models.oauth2_password_bearer_with_cookie import OAuth2PasswordBearerWithCookie
from datetime import datetime, timedelta, timezone
from ..services.email_services import EmailServices
from dotenv import load_dotenv
import os

load_dotenv()

class AuthenticationUsersServices():
    site_url = os.getenv("SITE_URL")
    _password_services=PasswordServices()
    _users_repository=UsersRepository()
    _token_services= TokenServices()
    _email_services=EmailServices()
    
    
    
    def authenticate_user(self, username:str, plain_password:str):
        user= UserValidationServices.check_user_validity(username)
        if user is None:
            return RedirectResponse(
                url=f'{self.site_url}/users/login?toast=invalid_credentials',
                status_code=status.HTTP_303_SEE_OTHER  
            )
        
            

        if not self._password_services.verify_password(user.password, plain_password):
            return RedirectResponse(
                url=f'{self.site_url}/users/login?toast=invalid_credentials',
                status_code=status.HTTP_303_SEE_OTHER
               
                
            )
        if user.disabled:
            return RedirectResponse(
                url=f'{self.site_url}/users/login?toast=disabled_account',
                status_code=status.HTTP_303_SEE_OTHER
          
                
            )
        
        if not user.is_verified and user.role_id == 2:
            self._email_services.send_email(user)
            return RedirectResponse(
                url=f'{self.site_url}/users/login?toast=email_not_verified',
                status_code=status.HTTP_303_SEE_OTHER
            )
            
        return user

    
    def handle_authentication(self, username, plain_password):
        user_autenticado=self.authenticate_user(username, plain_password)
        
        if isinstance(user_autenticado, RedirectResponse):
            return user_autenticado
        
        access_token=self._token_services.create_access_token(user_autenticado, user_autenticado.role.scopes)
        refresh_token=self._token_services.create_refresh_token(user_autenticado)
        auth_response=AuthResponse(access_token=access_token,refresh_token=refresh_token)
        
        return self.create_response_with_cookies(auth_response)
        

        
    def handle_refresh_access_token(self,user:User):
        access_token=self._token_services.create_access_token(user, user.role.scopes)
        return access_token
    
    
    def set_cookie(self,response:Response,key:str,token:str):
        response.set_cookie(
            key=key,
            value=f"Bearer {token}",
            domain=os.getenv("SITE_DOMAIN"),
            path="/",
            #max_age=None,
            secure=True,
            httponly=True,   
            samesite="lax",
            expires=datetime.now(timezone.utc)+timedelta(days=1)
        )
    
    def create_response_with_cookies(self, auth_response:AuthResponse)->Response:
        response=Response(status_code=status.HTTP_302_FOUND)
        self.set_cookie(response,"access_token", auth_response.access_token)
        self.set_cookie(response,"refresh_token", auth_response.refresh_token)
        response.headers["Location"] = os.getenv("SITE_URL")
        return response
   
        
    def get_authentication_cookies(self,request:Request):
        
        access_token= request.cookies.get("access_token")
        refresh_token=request.cookies.get("refresh_token")
        if access_token and refresh_token:
            return {"message": f"Access token is {access_token}, Refresh token is {refresh_token}"}
        elif access_token:
            return {"message": f"Access token is {access_token}, No refresh token found"}
        elif refresh_token:
            return {"message": f"No access token found, Refresh token is {refresh_token}"}
        else:
            return {"message": "No cookies found"}
        
    
    def delete_cookies(self, response:Response):
        response.set_cookie(key="access_token",value="", expires=0,path="/",domain=os.getenv("SITE_DOMAIN"))
        response.set_cookie(key="refresh_token", value="",expires=0,path="/",domain=os.getenv("SITE_DOMAIN"))
        return {"message": "Logged out"}
        
        
        
        
    
    


    
    

    

    
    
      
        
        