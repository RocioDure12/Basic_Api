from ..models.user import User
from ..models.role import Role
from ..repositories.users_repository import UsersRepository
from .password_services import PasswordServices
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
from ..models.auth_response import AuthResponse



                
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class AuthenticationHandler():
    _password_services=PasswordServices()
    _users_repository=UsersRepository()
    _auth_response=AuthResponse()
    
    
    
    def authenticate_user(self, username:str, plain_password:str):
        user= AuthenticationHandler.check_user_validity(username)
        if user and self._password_services.verify_password(user.password, plain_password):
            return user
    
    
    def handle_authentication(self, username, plain_password):
        user=self.authenticate_user(username, plain_password)
        if not user:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},)
        
        access_token=self.create_access_token(user, user.role.scopes)
        refresh_token=self.create_refresh_token(user)
        verification_token=self.create_verification_token(user)
        return AuthResponse(access_token=access_token,refresh_token=refresh_token, verification_token=verification_token)
    
    def handle_refresh_access_token(self,user:User):
        access_token=self.create_access_token(user, user.role.scopes)
        return access_token
    
    
    def create_token(self,
                     user:User, 
                     scopes:list[str],
                     expiration_minutes:int,
                     token_secret:str,
                     token_algorithm:str):
        expires_delta=timedelta(minutes=int(expiration_minutes))
        expiration_date=datetime.utcnow() + expires_delta
        data_to_encode = {
            "iat":datetime.utcnow(),
            "sub":user.username,
            "exp":expiration_date,
            #"scopes":scopes
        }
                
        encoded_jwt = jwt.encode(
            data_to_encode,
            token_secret, 
            algorithm=token_algorithm
        )
        return encoded_jwt   
    
    def create_access_token(self, user:User, scopes:list[str]):
        return self.create_token(user,
                                 scopes,
                                 expiration_minutes=os.getenv(f'JWT_ACCESS_TOKEN_EXPIRE_MINUTES'),
                                 token_secret=os.getenv(f'JWT_ACCESS_TOKEN_SECRET'),
                                 token_algorithm=os.getenv(f'JWT_ACCESS_TOKEN_ALGORITHM')
                                )
                                 
    
    def create_refresh_token(self, user:User):
        return self.create_token(user,
                                 [],
                                 expiration_minutes=os.getenv(f'JWT_REFRESH_TOKEN_EXPIRE_MINUTES'),
                                 token_secret=os.getenv(f'JWT_REFRESH_TOKEN_SECRET'),
                                 token_algorithm=os.getenv(f'JWT_REFRESH_TOKEN_ALGORITHM')
                                 )
        
    def create_verification_token(self, user:User):
        return self.create_token(user,
                                 [],
                                 expiration_minutes=os.getenv(f'JWT_VERIFICATION_TOKEN_EXPIRE_MINUTES'),
                                 token_secret=os.getenv(f'JWT_VERIFICATION_TOKEN_SECRET'),
                                 token_algorithm=os.getenv(f'JWT_VERIFICATION_TOKEN_ALGORITHM')
                                 )
    
    @staticmethod
    def check_token(security_scopes:SecurityScopes,
                            token:str,
                            jwt_secret:str,
                            jwt_algorithm:str
            
                            
                            ):
        if security_scopes.scopes:
            authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        else:
            authenticate_value = "Bearer"
            
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": authenticate_value},
        )

        try:
            payload = jwt.decode(
                token, 
                jwt_secret, 
                algorithms=[jwt_algorithm])

        except JWTError:
            raise credentials_exception
        
        username:str = payload.get('sub')
        if username is None:
            raise credentials_exception
        user=AuthenticationHandler.check_user_validity(username)
        
        scopes:list[str]= user.role.scopes #payload.get('scopes')
        AuthenticationHandler.check_scopes(security_scopes,scopes)
        
    
        return user
      
    
    @staticmethod
    def check_access_token(security_scopes:SecurityScopes,
                           token:Annotated[str, Depends(oauth2_scheme)]):
        return AuthenticationHandler.check_token(
                                security_scopes,
                                token=token,
                                jwt_secret=os.getenv(f'JWT_ACCESS_TOKEN_SECRET'),
                                jwt_algorithm=os.getenv(f'JWT_ACCESS_TOKEN_ALGORITHM')
                                )
    
    @staticmethod
    def check_refresh_token(security_scopes:SecurityScopes,
                           token:Annotated[str, Depends(oauth2_scheme)]):
        return AuthenticationHandler.check_token(
                                security_scopes,
                                token=token,
                                jwt_secret=os.getenv(f'JWT_REFRESH_TOKEN_SECRET'),
                                jwt_algorithm=os.getenv(f'JWT_REFRESH_TOKEN_ALGORITHM')
                                )
    
    @staticmethod
    def check_verification_token(security_scopes:SecurityScopes,
                           token:Annotated[str, Depends(oauth2_scheme)]):
        return AuthenticationHandler.check_token(
                                security_scopes,
                                token=token,
                                jwt_secret=os.getenv(f'JWT_VERIFICATION_TOKEN_SECRET'),
                                jwt_algorithm=os.getenv(f'JWT_VERIFICATION_TOKEN_ALGORITHM')
                                )
    @staticmethod
    def check_user_validity( username:str):
        user= UsersRepository().read_by_username(username)
        if user is None:
            raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Incorrect username or password",
                        headers={"WWW-Authenticate": "Bearer"},)
            
        if user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return user

    
    @staticmethod
    def check_scopes(security_scopes:SecurityScopes,scopes):
        required_scopes = security_scopes.scopes
        if required_scopes:
            for scope in required_scopes:
                if scope not in scopes:
                    raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": "Bearer"},
            )
    

    
    
      
        
        