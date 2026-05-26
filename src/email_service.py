import smtplib
import ssl
from email.message import EmailMessage
from logger import logger

class EmailService:
    def __init__(self, smtp_server, port, sender, password):
        self.smtp_server = smtp_server
        self.port = port
        self.sender = sender
        self.password = password

        self.context = ssl.create_default_context()

    def send_email(self, recipient, body, subject):
        msg = EmailMessage()

        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = recipient
        msg.set_content(body, subtype='html')

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=self.context) as server:
                server.login(self.sender, self.password)
                server.send_message(msg)
                logger.info(f'Email sent to {recipient}')
        except Exception as ex:
            logger.error(f'Error sending email to {recipient}: {ex}')