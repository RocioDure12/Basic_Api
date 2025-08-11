from fastapi import HTTPException
from ..models.user import User
from ..repositories.users_repository import UsersRepository
from ..services.token_services import TokenServices
from ..services.email_services import EmailServices


class Registration_UsersServices:
    _users_repository=UsersRepository()
    _token_services=TokenServices()
    _email_services=EmailServices()

    
    def verify_user(self, new_user: User):
        existing_user=self._users_repository.find_by_username_or_email(
            username=new_user.username, email=new_user.email
            )
        if not existing_user:
            return new_user
        
        if not existing_user.is_verified:
            existing_user.verification_code=self._token_services.generate_verification_token()
            self._users_repository.update(existing_user.id, existing_user)
            self._email_services.send_email(existing_user)
            raise HTTPException(
                status_code=409,
                detail="This account already exists but is not verified. A new verification email has been sent."
                
            )
        if existing_user.username == new_user.username:
            
            raise HTTPException(status_code=400, detail="Username already in use.")
        
        if existing_user.email == new_user.email:
            
            raise HTTPException(status_code=400, detail="Email already registered.")

        return new_user
        


    def user_registration(self, new_user: User):
        self.verify_user(new_user)
        new_user.verification_code = self._token_services.generate_verification_token()
        self._users_repository.create_user(new_user)
        self._email_services.send_email(new_user)
        return new_user
            
        
   
          
   


    
         
    
       

                
          
        
        