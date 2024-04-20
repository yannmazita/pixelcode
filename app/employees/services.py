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
    def __init__(self, session: Session):
        self.session = session


class EmployeeService:
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
        Compute the email verification code using the employee's code in the database.
        """
        state = self.get_employee_state(employee)
        prefix = state.employee_code_in_database[-2:]
        suffix = state.employee_code_in_database[-4:]
        email_code = prefix + hashlib.sha256(suffix.encode()).hexdigest()
        return email_code

    def generate_and_send_email(self, employee: EmployeeIdentity) -> None:
        """
        Generate an email verification code and send it to the employee's email.
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
        Generates a QR code for the given employee ID and saves it as a PNG file.
        """
        state = self.get_employee_state(employee)
        if not state.email_code_validated:
            raise ValueError("Email code not validated for employee.")
        img = qrcode.make(employee.employee_code)
        qr_code_path = f"app/static/qr_codes/{id}.png"
        img.save(qr_code_path)
        return qr_code_path

    def validate_email_code(self, employee: EmployeeIdentity, input_code: str) -> bool:
        """
        Validates the input email code against the computed one, updating the employee's state.
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
