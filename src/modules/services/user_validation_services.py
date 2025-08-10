from ..repositories.users_repository import UsersRepository
from fastapi import HTTPException, status
from fastapi.security import SecurityScopes


class UserValidationServices:
        @staticmethod
        def check_user_validity( username:str):
            return UsersRepository().read_by_username(username)
    
        
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