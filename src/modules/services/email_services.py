from email.message import EmailMessage
import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailServices:
    def send_email(self):
        SMTP_SERVER =os.getenv('SMTP_SERVER')
        SMTP_PORT =465
        SMTP_PASSWORD=os.getenv('EMAIL_PASSWORD')
        EMAIL_SENDER = os.getenv('EMAIL_SENDER')
        EMAIL_RECEIVER='rocioevelyndure@gmail.com'
        
        
        message=MIMEMultipart()
        message["From"] =EMAIL_SENDER
        message["Subject"] = "EMAIL VERIFICATION"
        
        body="Click the following link to verify your account: https://your-app.com/verify?token={token}"
        message.attach(MIMEText(body,"plain"))
        
        context=ssl.create_default_context()
        server=smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context)
        server.login(EMAIL_SENDER, SMTP_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, message.as_string())
        server.quit()
    
    
    def verify_email(self):
        pass
    