import hashlib
from fastapi import HTTPException, status
import qrcode
from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.employees.models import EmployeeIdentity, EmployeeState
from app.emails.services import EmailService
from app.database import engine


class EmployeeAdminService:
    """
    Service class for employee-related operations for admin users.

    This class provides methods to interact with the database and perform operations on employees for admin users.

    Attributes:
        session: The database session to be used for operations.
    """

    def __init__(self, session: Session):
        self.session = session


class EmployeeService:
    """
    Service class for employee-related operations.

    This class provides methods to interact with the database and perform operations on employees.

    Attributes:
        session: The database session to be used for operations.
        email_service: The email service to be used for sending emails.
    """

    def __init__(self, session: Session, email_service: EmailService):
        self.session = session
        self.email_service = email_service

    def get_employee_identity(self, id: UUID) -> EmployeeIdentity:
        """
        Retrieve an employee's identity information from the database.

        Args:
            id: The database ID of the employee.
        Returns:
            The employee's identity information.
        """
        try:
            employee = self.session.exec(
                select(EmployeeIdentity).where(EmployeeIdentity.id == id)
            ).one()
            return employee
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee does not exist",
            )

    def get_employee_identity_by_employee_id(
        self, employee_id: str
    ) -> EmployeeIdentity:
        """
        Retrieve an employee's identity information from the database using their employee ID.

        Args:
            employee_id: The employee ID of the employee.
        Returns:
            The employee's identity information.
        """
        try:
            employee = self.session.exec(
                select(EmployeeIdentity).where(
                    EmployeeIdentity.employee_id == employee_id
                )
            ).one()
            return employee
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee with given ID does not exist",
            )

    def get_employee_identity_by_email(self, email: str) -> EmployeeIdentity:
        """
        Retrieve an employee's identity information from the database using their email.

        Args:
            email: The email of the employee.
        Returns:
            The employee's identity information.
        """
        try:
            employee = self.session.exec(
                select(EmployeeIdentity).where(EmployeeIdentity.employee_email == email)
            ).one()
            return employee
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee with given email does not exist",
            )

    def get_employee_state(self, employee: EmployeeIdentity) -> EmployeeState:
        """
        Retrieve an employee's state information from the database.

        Args:
            employee: The employee whose state information is to be retrieved.
        Returns:
            The employee's state information.
        """
        try:
            state = self.session.exec(
                select(EmployeeState).where(EmployeeState.id == employee.id)
            ).one()
            return state
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No state found for employee ID: {id}",
            )

    def compute_email_code(self, employee: EmployeeIdentity) -> str:
        """
        Compute the email verification code for the given employee.
        Args:
            employee: The employee for which the code is to be computed.
        Returns:
            The computed email code.
        """
        state = self.get_employee_state(employee)
        prefix = state.employee_code_in_database[-2:]
        suffix = state.employee_code_in_database[-4:]
        email_code = prefix + hashlib.sha256(suffix.encode()).hexdigest()
        return email_code

    def generate_and_send_email(self, employee: EmployeeIdentity) -> None:
        """
        Generates an email code for the given employee and sends it to their email address.
        Args:
            employee: The employee to whom the email is to be sent.
        """
        email_code = self.compute_email_code(employee)
        email_message = self.email_service.create_email(
            employee.employee_email, email_code
        )
        self.email_service.send_email(email_message, employee.employee_email)
        state = self.get_employee_state(employee)
        state.email_code_sent = True

        with Session(engine) as session:
            session.add(state)
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update employee state",
                )

    def create_qr_code(self, employee: EmployeeIdentity) -> str:
        """
        Creates a QR code for the given employee.
        Args:
            employee: The employee for whom the QR code is to be created.
        Returns:
            The path to the created QR code.
        """
        state = self.get_employee_state(employee)
        if not state.email_code_validated:
            raise ValueError("Email code not validated for employee.")
        img = qrcode.make(employee.employee_code)
        qr_code_path = f"app/static/qr_codes/{employee.employee_id}.png"
        img.save(qr_code_path)
        return qr_code_path

    def validate_email_code(self, employee: EmployeeIdentity, input_code: str) -> bool:
        """
        Validates the email code entered by the employee.
        Args:
            employee: The employee for whom the email code is to be validated.
            input_code: The email code entered by the employee.
        Returns:
            True if the email code is valid, False otherwise.
        """
        expected_code = self.compute_email_code(employee)
        state = self.get_employee_state(employee)
        if input_code == expected_code:
            state.email_code_validated = True
            with Session(engine) as session:
                session.add(state)
                try:
                    session.commit()
                except IntegrityError:
                    session.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to update employee state",
                    )
            return True
        return False
