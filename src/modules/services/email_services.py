from dotenv import load_dotenv
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from ..models.user import User
from ..repositories.users_repository import UsersRepository
import smtplib
from email.message import EmailMessage
from loguru import logger



load_dotenv()

class EmailServices():
    def __init__(self):
        self._users_repository = UsersRepository()

    def send_email(self, user: User):
        logger.debug('Sending email')
        logger.debug('Preparing message')
        # Contenido del correo
        subject = "Verify your TaskPlanner account"
        html_content = f"""
            <p>Hello {user.name if user.name else ''},</p>
            <p>Click the following link to verify your account:</p>
            <a href="http://localhost:5173/verifyemail/{user.verification_code}">
                Verify your account
            </a>
            <p>If you did not request this, please ignore this email.</p>
        """
        text_content = f"""
            Hello {user.name if user.name else ''},
            Click the following link to verify your account:
            http://localhost:5173/verifyemail/{user.verification_code}
            If you did not request this, please ignore this email.
        """

        # TODO: Refactorizar urgente. Utilizar libreria de sendgrid. https://pypi.org/project/sendgrid/1.6.22/

        msg = EmailMessage()
        msg.set_content(text_content)
        msg['From'] = 'taskplannerapp@hotmail.com'
        msg['To'] =  user.email
        msg['Subject'] = subject
        logger.debug(msg)

        with  smtplib.SMTP_SSL('smtp.sendgrid.net') as smtp:
            smtp.login('apikey', os.getenv("API_KEY_SEND_GRID"))
            logger.debug('Sending email')
            reply = smtp.sendmail(msg['From'], msg['To'], msg.as_string())
            logger.debug('Reply',reply)
        logger.debug('Email sent')

        '''
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": user.email, "name": user.name or "User"}],
            sender={"name": self.sender_name, "email": self.sender_email},
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )

        try:
            response = self.api_instance.send_transac_email(send_smtp_email)
            print(f"Email sent successfully to {user.email}: {response}")
        except ApiException as e:
            print(f"Error sending email: {e}")
        '''

    def verify_email(self, token: str):
        user = self._users_repository.get_by_verification_token(token)
        if user is not None:
            user.is_verified = True
            self._users_repository.update(user.id, user)
        return user
