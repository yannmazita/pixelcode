import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailService:
    def __init__(self):
        self.server_address: str = os.getenv("SMTP_SERVER_ADDRESS")  # type: ignore
        self.port: int = os.getenv("SMTP_PORT")  # type: ignore
        self.email_address: str = os.getenv("SMTP_EMAIL_ADDRESS")  # type: ignore
        self.password: str = os.getenv("SMTP_SERVER_PASSWORD")  # type: ignore
        self.context = ssl.create_default_context()

    def send_email(self, message: MIMEMultipart, receiver_email: str) -> None:
        with smtplib.SMTP_SSL(
            self.server_address, self.port, context=self.context
        ) as server:
            server.login(self.email_address, self.password)
            server.sendmail(self.email_address, receiver_email, message.as_string())

    def create_email(self, receiver_email: str, email_code: str) -> MIMEMultipart:
        """
        Creates an email message to be sent to the employee.
        """
        message = MIMEMultipart("alternative")
        message["From"] = self.email_address
        message["To"] = receiver_email
        message["Subject"] = "Email Verification Code"
        body = MIMEText(f"Your email verification code is {email_code}", "plain")
        message.attach(body)
        return message
