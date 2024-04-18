import hashlib
import os
import smtplib
import ssl
import qrcode
from uuid import UUID
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.exceptions import NoEmployeeInstance


class Employee:
    """
    An employee in the company.

    Attributes:
        employee_email: The email of the employee.
        employee_code_in_database: The employee code in the database.
        email_code_validated: Whether the email code has been validated.
        email_code_sent: Whether the email code has been sent.
    """

    def __init__(self):
        self.employee_email: str = ""
        self.employee_code_in_database: str = ""
        self.email_code_validated: bool = False
        self.email_code_sent: bool = False


class Employees:
    """The employees manager.

    Attributes:
        employees: The employees in the company.
    """

    def __init__(self):
        self.employees: dict[UUID, Employee] = {}

    def create_employee_instance(self, user_id: UUID) -> None:
        """
        Creates an employee instance.

        Args:
            user_id: The ID of the user.
        """
        self.employees[user_id] = Employee()

    def remove_employee_instance(self, user_id: UUID) -> None:
        """
        Removes an employee instance.

        Args:
            user_id: The ID of the user.
        """
        if user_id not in self.employees:
            raise NoEmployeeInstance(user_id)
        self.employees.pop(user_id)

    def get_employee_instance(self, user_id: UUID) -> Employee:
        """
        Gets an employee instance.

        Args:
            user_id: The ID of the user.

        Returns:
            The employee instance.
        """
        if user_id not in self.employees:
            raise NoEmployeeInstance(user_id)
        return self.employees[user_id]

    def compute_email_code(self, user_id: UUID) -> str:
        """
        Computes the email code.
        Args:
            user_id: The ID of the user.
        Returns:
            The email code.
        """
        employee: Employee = self.get_employee_instance(user_id)
        prefix: str = employee.employee_code_in_database[-2:]
        suffix: str = employee.employee_code_in_database[-4:]
        return prefix + hashlib.sha256(suffix.encode()).hexdigest()

    def check_email_code(self, user_id: UUID, email_code: str) -> bool:
        """
        Checks the email code.
        Args:
            user_id: The ID of the user.
            email_code: The code sent by email.
        Returns:
            Whether the email code is correct.
        """
        computed_email_code: str = self.compute_email_code(user_id)

        if email_code == computed_email_code:
            employee: Employee = self.get_employee_instance(user_id)
            employee.email_code_validated = True
            return True
        return False


class Email:
    """
    An email message.

    Attributes:
        message: The email message.
    """

    EMAIL_ADDRESS: str = os.getenv("SMTP_EMAIL_ADDRESS")  # type: ignore

    def __init__(self):
        self.message: MIMEMultipart = MIMEMultipart()

    def create_email(self, receiver_email: str, email_code: str) -> None:
        """
        Creates an email message.

        This method creates an email message with the given receiver email and email code.

        Args:
            receiver_email: The email address of the receiver.
            email_code: The email verification code.
        """
        sender_email: str = self.EMAIL_ADDRESS
        self.receiver_email: str = receiver_email
        self.message["From"] = sender_email
        self.message["To"] = receiver_email
        self.message["Subject"] = "Email Verification Code"
        self.message.attach(
            MIMEText(f"Your email verification code is {email_code}", "plain")
        )


class EmailClient:
    """
    An email client.

    Attributes:
        server_address: The address of the SMTP server.
        port: The port of the SMTP server.
        email_address: The email address of the sender.
        password: The password of the email account.
        server: The SMTP server connection.
    """

    def __init__(self):
        self.server_address: str = os.getenv("SMTP_SERVER_ADDRESS")  # type: ignore
        self.port: int = os.getenv("SMTP_PORT")  # type: ignore
        self.email_address: str = os.getenv("SMTP_EMAIL_ADDRESS")  # type: ignore
        self.password: str = os.getenv("SMTP_SERVER_PASSWORD")  # type: ignore
        self.server: smtplib.SMTP_SSL | None = None
        self.context = ssl.create_default_context()

    def send_email(self, message: MIMEMultipart, receiver_email: str) -> None:
        """
        Args:
            message: The email message to send.
            receiver_email: The recipient's email address.
        """
        with smtplib.SMTP_SSL(
            self.server_address, self.port, context=self.context
        ) as server:
            server.login(self.email_address, self.password)
            server.sendmail(self.email_address, receiver_email, message.as_string())


class PixelCode:
    """
    The PixelCode class.

    Attributes:
        employees: The employees manager.
        email_client: The email client.
    """

    def __init__(self):
        self.employees: Employees = Employees()
        self.email_client: EmailClient = EmailClient()

    def create_qr_code(self, user_id: UUID) -> None:
        """
        Creates a QR code.

        This method generates a QR code for the given user ID and saves it as a PNG file.
        Args:
            user_id: The ID of the user.
        """
        employee: Employee = self.employees.get_employee_instance(user_id)
        code: str = employee.employee_code_in_database
        img = qrcode.make(code)
        img.save(f"app/static/qr_codes/{user_id}.png")

    def generate_and_send_email(self, user_id: UUID) -> None:
        """
        Generates and sends an email.
        Args:
            user_id: The ID of the user.
        """
        employee: Employee = self.employees.get_employee_instance(user_id)
        email_code: str = self.employees.compute_email_code(user_id)
        email: Email = Email()
        email.create_email(employee.employee_email, email_code)
        message = email.message
        self.email_client.send_email(message, employee.employee_email)
