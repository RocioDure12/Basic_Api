from fastapi import HTTPException
from ..models.user import User
from ..repositories.users_repository import UsersRepository
from ..services.token_services import TokenServices
from ..services.email_services import EmailServices

"""
def verification_email(email):
    subject = "Account Verification"
    body = f"Click the following link to verify your account: https://your-app.com/verify?token={token}"

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] ="smtp.gmail.com"
    message["To"] = email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(EMAIL_SENDER, [email], message.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending verification email: {str(e)}")
        
"""
class Registration_UsersServices:
    _users_repository=UsersRepository()
    _token_services=TokenServices()
    _email_services=EmailServices()
    
    def verify_user(self,new_user:User):
        users=self._users_repository.read()
        for user in users:
                    if user.username == new_user.username:
                        raise HTTPException(status_code=400, detail="The username is already in use. Please choose another username")
                    if user.email == new_user.email:
                        raise HTTPException(status_code=400, detail="The email address is already registered. Please use a different email address")
        
        return new_user            
        
        
        
    def handle_account_registration(self, new_user:User):
        self.verify_user(new_user)
        new_user.verification_code=self._token_services.generate_verification_token()
        self._users_repository.create(new_user)
        #enviar email de verificacion al nuevo user
        self._email_services.send_email(new_user)
        
       

                
                #if item.is_verified is False:
                 #       raise HTTPException(status_code=400, detail="Account not verified")
         


              


    

    
        
        