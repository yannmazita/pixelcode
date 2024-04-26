import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailService:
    """
    Services for sending emails to employees.

    This class is responsible for sending emails to employees.
    It uses the SMTP server provided in the environment variables to send emails.

    Attributes:
        server_address: The address of the SMTP server.
        port: The port of the SMTP server.
        email_address: The email address of the sender.
    """

    def __init__(self):
        self.server_address: str = os.getenv("SMTP_SERVER_ADDRESS")  # type: ignore
        self.port: int = os.getenv("SMTP_PORT")  # type: ignore
        self.email_address: str = os.getenv("SMTP_EMAIL_ADDRESS")  # type: ignore

    def send_email(self, message: MIMEMultipart, receiver_email: str) -> None:
        """
        Sends an email to the employee.

        Args:
            message: The email message to be sent.
            receiver_email: The email address of the employee.
        """
        with smtplib.SMTP(self.server_address, self.port) as server:
            server.sendmail(self.email_address, receiver_email, message.as_string())

    def create_email(self, receiver_email: str, email_code: str) -> MIMEMultipart:
        """
        Creates an email message to be sent to the employee.

        Args:
            receiver_email: The email address of the employee.
            email_code: The verification code to be sent.
        Returns:
            The email message to be sent.
        """
        message = MIMEMultipart("alternative")
        message["From"] = self.email_address
        message["To"] = receiver_email
        message["Subject"] = "Email Verification Code"
        body = MIMEText(f"Your email verification code is {email_code}", "plain")
        message.attach(body)
        return message


class EmailServiceSecure(EmailService):
    """
    Services for sending emails to employees securely.

    This class is responsible for sending emails to employees securely.
    It uses the SMTP server provided in the environment variables to send emails securely.

    Attributes:
        password: The password of the sender's email address.
        context: The SSL context to use for the connection.
    """

    def __init__(self):
        super().__init__()
        self.password: str = os.getenv("SMTP_SERVER_PASSWORD")  # type: ignore
        self.context = ssl.create_default_context()

    def send_email(self, message: MIMEMultipart, receiver_email: str) -> None:
        with smtplib.SMTP_SSL(
            self.server_address, self.port, context=self.context
        ) as server:
            server.login(self.email_address, self.password)
            server.sendmail(self.email_address, receiver_email, message.as_string())
