from email.message import EmailMessage
import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..models.user import User
from ..repositories.users_repository import UsersRepository
from fastapi import  HTTPException

class EmailServices():
    def __init__(self):
        self._users_repository=UsersRepository()
        
    def send_email(self, user:User):
        SMTP_SERVER =os.getenv('SMTP_SERVER')
        SMTP_PORT =465
        SMTP_PASSWORD=os.getenv('EMAIL_PASSWORD')
        EMAIL_SENDER = os.getenv('EMAIL_SENDER')
        EMAIL_RECEIVER=user.email
        
        
        message=MIMEMultipart()
        message["From"] =EMAIL_SENDER
        message["Subject"] = "EMAIL VERIFICATION"
        
        body=f"Click the following link to verify your account:{user.verification_code}"
        message.attach(MIMEText(body,"plain"))
        
        context=ssl.create_default_context()
        server=smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context)
        server.login(EMAIL_SENDER, SMTP_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, message.as_string())
        server.quit()
    

    def verify_email(self, user:User):
        user=self._users_repository.get_by_verification_token(user.verification_code)
        if user is not None:
            user.is_verified=True
            self._users_repository.update(user.id,user)
        return user
      
      
 
    
        
        
        
        
    