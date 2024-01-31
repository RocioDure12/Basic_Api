from fastapi import HTTPException
from ..models.user import User
from ..repositories.users_repository import UsersRepository

from email.message import EmailMessage
import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


     
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
class UsersServices:
    _users_repository=UsersRepository()
    
    
    def handle_account_registration(self,item:User):
                users=self._users_repository.read()
                for user in users:
                    if user.username == item.username:
                        raise HTTPException(status_code=400, detail="The username is already in use. Please choose another username")
                    if user.email == item.email:
                        raise HTTPException(status_code=400, detail="The email address is already registered. Please use a different email address")
                                  
                #item.verification_code=self.generate_verification_code()
                self._users_repository.create(item)
                
                if item.is_verified is False:
                        raise HTTPException(status_code=400, detail="Account not verified")



    

    
        
        