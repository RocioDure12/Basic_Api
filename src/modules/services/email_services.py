from dotenv import load_dotenv
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from ..models.user import User
from ..repositories.users_repository import UsersRepository
from loguru import logger

load_dotenv()

class EmailServices():
    def __init__(self):
        self._users_repository = UsersRepository()

    def send_email(self, user: User):
        logger.debug('Sending email using SendGrid')

        subject = "Verify your TaskPlanner account"
        verification_link = f"http://localhost:5173/verifyemail/{user.verification_code}"

        html_content = f"""
            <p>Hello {user.name},</p>
            <p>Click the following link to verify your account:</p>
            <a href="{verification_link}">{verification_link}</a>
            <p>If you did not request this, please ignore this email.</p>
        """

        message = Mail(
            from_email='taskplannerapp@hotmail.com',  # este correo debe estar verificado en SendGrid
            to_emails=user.email,
            subject=subject,
            html_content=html_content
        )
        try:
            sg = SendGridAPIClient(os.getenv("API_KEY_SEND_GRID"))
            logger.debug(f"Sending message...")
            response = sg.send(message)
            logger.debug(f"Email sent: Status {response.status_code}")
        except Exception as e:
            
            logger.error(f"Error sending email: {e}")

    def verify_email(self, token: str):
        user = self._users_repository.get_by_verification_token(token)
        if user is not None:
            user.is_verified = True
            self._users_repository.update(user.id, user)
        return user
