import smtplib
from email.mime.text import MIMEText
from ..repositories.users_repository import UsersRepository
from ..models.user import User
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

class EmailServices:
    def __init__(self):
        self._users_repository = UsersRepository()
      

    def send_email(self, user: User):
        remitente = "taskplannerapplication@gmail.com"
        destinatario = user.email
        contraseña_app = os.getenv("PASSWORD_EMAIL")

        # Crear el mensaje
        mensaje = MIMEMultipart()
        mensaje['From'] = remitente
        mensaje['To'] = destinatario
        mensaje['Subject'] = "Asunto del correo"

        api_url = os.getenv("API_URL")
        cuerpo =f'Haz clic en el siguiente enlace para verificar tu cuenta: {api_url}/verifyemail/{user.verification_code}. Si no solicitaste esto, ignora este correo'

        mensaje.attach(MIMEText(cuerpo, 'html'))

        try:
            print("Enviando email a ", destinatario)
            # Conexión con servidor SMTP Gmail usando TLS
            servidor = smtplib.SMTP('smtp.gmail.com', 587)
            servidor.starttls()  # Inicia TLS (seguridad)

            # Login con usuario y contraseña de aplicación
            servidor.login(remitente, contraseña_app)
            
            # Enviar email
            servidor.sendmail(remitente, destinatario, mensaje.as_string())

            # Cerrar conexión
            servidor.quit()

            print("Correo enviado correctamente!")

        except Exception as e:
            print(f"Error al enviar correo: {e}")
            
            
    def verify_email(self, token: str):
        user = self._users_repository.get_by_verification_token(token)
        if user:
            user.is_verified = True
            user.disabled=False
            self._users_repository.update(user.id, user)
        return user