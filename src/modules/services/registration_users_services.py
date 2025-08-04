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
        users = self._users_repository.read()
        for user in users:
            if user.username == new_user.username or user.email == new_user.email:
                if not user.is_verified:
                    # Reenviar email con nuevo token
                    user.verification_code = self._token_services.generate_verification_token()
                    self._users_repository.update(user)
                    self._email_services.send_email(user)
                    raise HTTPException(
                        status_code=409,
                        detail="This account already exists but is not verified. A new verification email has been sent."
                    )
                else:
                    # Usuario ya existe y está verificado
                    if user.username == new_user.username:
                        raise HTTPException(status_code=400, detail="The username is already in use. Please choose another username.")
                    if user.email == new_user.email:
                        raise HTTPException(status_code=400, detail="The email address is already registered. Please use a different email address.")

        return new_user


    def user_registration(self, new_user:User):
            self.verify_user(new_user)
            new_user.verification_code=self._token_services.generate_verification_token()
            self._users_repository.create_user(new_user)
            self._email_services.send_email(new_user)
            return new_user
          
        
   
          
   


    
         
    
       

                
          
        
        