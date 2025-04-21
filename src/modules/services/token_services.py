from fastapi import Depends, HTTPException, status
from fastapi.security import  SecurityScopes
from jose import JWTError, jwt
import os
from typing import Annotated
from ..services.user_validation_services import UserValidationServices
from fastapi.security import OAuth2PasswordBearer,SecurityScopes
from ..models.user import User
from datetime import datetime, timedelta
from ..models.user import User
import secrets
from ..models.oauth2_password_bearer_with_cookie import OAuth2PasswordBearerWithCookie

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# TODO: cargar desde el .env
oauth2_scheme = OAuth2PasswordBearerWithCookie(loginUrl="users/login")

class TokenServices:
    
    def generate_verification_token(self):
        return secrets.token_hex(32)
    
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
            user=UserValidationServices.check_user_validity(username)
            
            scopes:list[str]= user.role.scopes 
            UserValidationServices.check_scopes(security_scopes,scopes)
            
        
            return user
        
       
    @staticmethod
    def check_access_token(security_scopes:SecurityScopes,
                            token:Annotated[str, Depends(oauth2_scheme)]):
            return TokenServices.check_token(
                                    security_scopes,
                                    token=token,
                                    jwt_secret=os.getenv(f'JWT_ACCESS_TOKEN_SECRET'),
                                    jwt_algorithm=os.getenv(f'JWT_ACCESS_TOKEN_ALGORITHM')
                                    )
        
    @staticmethod
    def check_refresh_token(security_scopes:SecurityScopes,
                            token:Annotated[str, Depends(oauth2_scheme)]):
            return TokenServices.check_token(
                                    security_scopes,
                                    token=token,
                                    jwt_secret=os.getenv(f'JWT_REFRESH_TOKEN_SECRET'),
                                    jwt_algorithm=os.getenv(f'JWT_REFRESH_TOKEN_ALGORITHM')
                                    )
    
       



        
        