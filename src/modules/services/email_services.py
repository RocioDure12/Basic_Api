from mailersend import emails
from dotenv import load_dotenv
import os
from ..models.user import User
from ..repositories.users_repository import UsersRepository

load_dotenv()

class EmailServices():
    def __init__(self):
        self._users_repository = UsersRepository()
        self.mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))

    def send_email(self, user: User):
        mail_body = {}

        mail_from = {
            "name": "TaskPlanner App",
            "email": "taskplannerapp@hotmail.com",  
        }

        recipients = [
            {
                "name": user.name if user.name else "User",
                "email": user.email,
            }
        ]

        reply_to = {
            "name": "TaskPlanner Support",
            "email": "taskplannerapp@hotmail.com",  #
        }

        subject = "Verify your TaskPlanner account"
        html_content = f"""
            <p>Hello {user.name if user.name else ''},</p>
            <p>Click the following link to verify your account:</p>
            <a href="http://localhost:5173/verifyemail/{user.verification_code}">
                Verify your account
            </a>
            <p>If you did not request this, please ignore this email.</p>
        """
        plaintext_content = f"""
            Hello {user.name if user.name else ''},
            Click the following link to verify your account:
            http://localhost:5173/verifyemail/{user.verification_code}
            If you did not request this, please ignore this email.
        """

        # Configurar el correo
        self.mailer.set_mail_from(mail_from, mail_body)
        self.mailer.set_mail_to(recipients, mail_body)
        self.mailer.set_subject(subject, mail_body)
        self.mailer.set_html_content(html_content, mail_body)
        self.mailer.set_plaintext_content(plaintext_content, mail_body)
        self.mailer.set_reply_to(reply_to, mail_body)

        # Enviar correo
        try:
            response = self.mailer.send(mail_body)
            print(f"Email sent! Status: {response['status_code']}, Data: {response['data']}")
        except Exception as e:
            print(f"Error sending email: {str(e)}")

    def verify_email(self, token: str):
        user = self._users_repository.get_by_verification_token(token)
        if user is not None:
            user.is_verified = True
            self._users_repository.update(user.id, user)
        return user

      
 
    
        
        
        
        
    