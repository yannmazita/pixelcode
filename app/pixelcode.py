import hashlib
import json
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
    """The employees manager."""

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
        try:
            self.employees.pop(user_id)
        except KeyError:
            raise NoEmployeeInstance(user_id)

    def get_employee_instance(self, user_id: UUID) -> Employee:
        """
        Gets an employee instance.

        Args:
            user_id: The ID of the user.

        Returns:
            The employee instance.
        """
        try:
            return self.employees[user_id]
        except KeyError:
            raise NoEmployeeInstance(user_id)

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
    EMAIL_ADDRESS: str = json.loads(os.getenv("SMTP_EMAIL_ADDRESS"))  # type: ignore

    def __init__(self):
        self.message: MIMEMultipart = MIMEMultipart()

    def create_email(
        self, user_id: UUID, employees: Employees, email_code: str
    ) -> None:
        employee: Employee = employees.get_employee_instance(user_id)
        sender_email: str = self.EMAIL_ADDRESS
        receiver_email: str = employee.employee_email
        self.message["From"] = sender_email
        self.message["To"] = receiver_email
        self.message["Subject"] = "Email Verification Code"
        self.message.attach(
            MIMEText(f"Your email verification code is {email_code}", "plain")
        )


class EmailClient:
    PASSWORD: str = json.loads(os.getenv("SMTP_SERVER_PASSWORD"))  # type: ignore
    PORT: int = json.loads(os.getenv("SMTP_PORT"))  # type: ignore
    SERVER_ADDRESS: str = json.loads(os.getenv("SMTP_SERVER_ADDRESS"))  # type: ignore
    EMAIL_ADDRESS: str = json.loads(os.getenv("SMTP_EMAIL_ADDRESS"))  # type: ignore

    def __init__(self):
        self.server: smtplib.SMTP_SSL | None = None

    def connect(self):
        """Establishes a reusable SMTP connection."""
        if not self.server:
            context = ssl.create_default_context()
            self.server = smtplib.SMTP_SSL(
                self.SERVER_ADDRESS, self.PORT, context=context
            )
            self.server.login(self.EMAIL_ADDRESS, self.PASSWORD)

    def disconnect(self):
        """Closes the SMTP connection."""
        if self.server:
            self.server.quit()
            self.server = None

    def send_email(self, message: MIMEMultipart, receiver_email: str) -> None:
        """
        Sends an email using a reusable SMTP connection.
        Args:
            message: The email message to send.
            receiver_email: The recipient's email address.
        """
        self.connect()
        assert self.server is not None
        self.server.sendmail(self.EMAIL_ADDRESS, receiver_email, message.as_string())
        self.disconnect()


class PixelCode:
    def __init__(self):
        self.employees: Employees = Employees()
        self.email_client: EmailClient = EmailClient()

    def create_qr_code(self, user_id: UUID) -> None:
        """
        Creates a QR code.
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
        email.create_email(user_id, self.employees, email_code)
        message = email.message
        self.email_client.send_email(message, employee.employee_email)
