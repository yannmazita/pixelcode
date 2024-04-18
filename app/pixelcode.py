from uuid import UUID
import hashlib, requests, asyncio, qrcode, csv

from app.exceptions import NoEmployeeInstance


class Employee:
    """
    An employee in the company.

    Attributes:
        employee_code_in_database: The employee code in the database.
        email_code_validated: Whether the email code has been validated.
        email_code_sent: Whether the email code has been sent.
    """

    def __init__(self):
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


class PixelCode:
    def __init__(self):
        self.employees: Employees = Employees()

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

    def send_email_code(self, user_id: UUID) -> None:
        """
        Sends the email code.
        Args:
            user_id: The ID of the user.
        """
        employee: Employee = self.employees.get_employee_instance(user_id)
        email_code: str = self.employees.compute_email_code(user_id)
