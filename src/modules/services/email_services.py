from email.message import EmailMessage
import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..models.user import User
from ..repositories.users_repository import UsersRepository
from fastapi import HTTPException
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class EmailServices():
    def __init__(self):
        self._users_repository = UsersRepository()
        
    def send_email(self, user: User):
        message = Mail(
            from_email='rooci_16@hotmail.com.ar',  # Asegúrate de usar un correo verificado en SendGrid
            to_emails=user.email,  # Pasamos solo el string o lista con el email
            subject='Sending with Twilio SendGrid is Fun',
            html_content=f'Click the following link to verify your account: http://localhost:5173/verifyemail/{user.verification_code}'
        )
        try:
            sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(f"Error: {str(e)}")


    
    def verify_email(self, token:str):
        user=self._users_repository.get_by_verification_token(token)
        if user is not None:
            user.is_verified=True
            self._users_repository.update(user.id,user)
            
        return user
   
      
      
 
    
        
        
        
        
    