from fastapi import HTTPException
from ..models.user import User
from ..repositories.users_repository import UsersRepository
import secrets
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
    
    
    
    
    def enviar_correo(self):
        SMTP_SERVER =os.getenv('SMTP_SERVER')
        SMTP_PORT =465
        SMTP_PASSWORD=os.getenv('EMAIL_PASSWORD')
        EMAIL_SENDER = os.getenv('EMAIL_SENDER')
        EMAIL_RECEIVER='gabrielmacus@gmail.com'
        
        
        message=MIMEMultipart()
        message["From"] =EMAIL_SENDER
        receiver_email=EMAIL_RECEIVER
        password=SMTP_PASSWORD
        message["Subject"] = "EMAIL VERIFICATION"
        
        body="popo"
        message.attach(MIMEText(body,"plain"))
        
        context=ssl.create_default_context()
        server=smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context)
        server.login(EMAIL_SENDER, SMTP_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, message.as_string())
        server.quit()
        print("Correo electrónico enviado exitosamente.")
    
    def handle_account_registration(self,item:User):
                users=self._users_repository.read()
                for user in users:
                    if user.username == item.username:
                        raise HTTPException(status_code=400, detail="The username is already in use. Please choose another username")
                    if user.email == item.email:
                        raise HTTPException(status_code=400, detail="The email address is already registered. Please use a different email address")
                    
                item.verification_code=self.generate_verification_code()
                return self._users_repository.create(item)


    def generate_verification_code(self):
     #Genera un código aleatorio y seguro
        return secrets.token_hex(32)
    
    def send_email(self):
        SMTP_SERVER =os.getenv('SMTP_SERVER')
        SMTP_PORT = 587
        SMTP_USERNAME =os.getenv('EMAIL_SENDER')
        SMTP_PASSWORD=os.getenv('EMAIL_PASSWORD')
        EMAIL_SENDER = os.getenv('EMAIL_SENDER')
        
        # Verifica que las credenciales no sean nulas
        if SMTP_USERNAME is None or SMTP_PASSWORD is None or EMAIL_SENDER is None:
            raise ValueError("Las credenciales de correo no están configuradas correctamente.")

        # Crea un objeto MIME para el correo electrónico
        message = MIMEMultipart()
        message["Subject"] = "Asunto del correo"
        message["From"] = SMTP_USERNAME
        message["To"] = "rocioevelyndure@gmail.com"

        # Cuerpo del correo en formato HTML
        body_html = """
            <html>
                <body>
                    <p>Contenido del correo en formato HTML.</p>
                </body>
            </html>
        """

        # Adjunta el cuerpo HTML al mensaje
        message.attach(MIMEText(body_html, "html"))

        try:
            # Conéctate al servidor SMTP
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                # Inicia TLS para una comunicación segura
                server.starttls()
                
                # Inicia sesión en el servidor de correo
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                
                # Envía el correo electrónico
                server.sendmail(EMAIL_SENDER, ["correo_destino@example.com"], message.as_string())
        except Exception as e:
            print(f"Error al enviar el correo: {str(e)}")

        
        