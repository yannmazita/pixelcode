import hashlib
from fastapi import HTTPException, status
from pydantic import EmailStr
import qrcode
from uuid import UUID, uuid4
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError, NoResultFound

from app.employees.models import (
    Employee,
    EmployeeCreate,
    EmployeeState,
)
from app.emails.services import EmailService


class EmployeeServiceBase:
    def __init__(self, session: Session):
        self.session = session

    def get_employee_by_internal_id(self, internal_id: str) -> Employee:
        """
        Retrieve an employee's identity information from the database using their employee ID.

        Args:
            internal_id: The employee ID of the employee.
        Returns:
            The employee's identity information.
        """
        try:
            employee = self.session.exec(
                select(Employee).where(Employee.internal_id == internal_id)
            ).one()
            return employee
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee with given ID does not exist",
            )

    def get_employee_by_email(self, email: EmailStr | None) -> Employee:
        """
        Retrieve an employee's identity information from the database using their email.

        Args:
            email: The email of the employee.
        Returns:
            The employee's identity information.
        """
        try:
            employee = self.session.exec(
                select(Employee).where(Employee.email == email)
            ).one()
            return employee
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee with given email does not exist",
            )

    def get_employee_state(self, employee: Employee) -> EmployeeState:
        """
        Retrieve an employee's state information from the database.

        Args:
            employee: The employee whose state information is to be retrieved.
        Returns:
            The employee's state information.
        """
        try:
            state = self.session.exec(
                select(EmployeeState).where(
                    EmployeeState.internal_id == employee.internal_id
                )
            ).one()
            return state
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No state found for employee ID: {id}",
            )


class EmployeeAdminService(EmployeeServiceBase):
    """
    Service class for employee-related operations for admin users.

    This class provides methods to interact with the database and perform operations on employees for admin users.

    Attributes:
        session: The database session to be used for operations.
    """

    def __init__(self, session: Session):
        super().__init__(session)

    def create_new_employee(self, employee: EmployeeCreate) -> Employee:
        """
        Create a new employee in the database.
        Args:
            employee: The employee to be created.
        Returns:
            The created employee.
        """
        try:
            self.session.exec(
                select(Employee).where(Employee.internal_id == employee.internal_id)
            ).one()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee with given ID already exists",
            )
        except NoResultFound:
            pass

        new_employee: Employee = Employee(
            id=uuid4(),
            internal_id=employee.internal_id,
            email=employee.email,
            code_to_print=employee.code_to_print,
            surname=employee.surname,
            firstname=employee.firstname,
        )
        db_employee = Employee.model_validate(new_employee)

        self.session.add(db_employee)
        self.session.commit()

        return db_employee

    def get_employee(self, id: UUID) -> Employee:
        """
        Retrieve an employee's identity information from the database.

        Args:
            id: The database ID of the employee.
        Returns:
            The employee's identity information.
        """
        try:
            employee = self.session.exec(
                select(Employee).where(Employee.id == id)
            ).one()
            return employee
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee does not exist",
            )

    def get_employees(self, offset: int = 0, limit: int = 100):
        """
        Retrieve a list of employees from the database.

        Args:
            offset: The number of records to skip.
            limit: The maximum number of records to return.
        Returns:
            A list of employees.
        """
        employees = self.session.exec(
            select(Employee).offset(offset).limit(limit)
        ).all()
        return employees

    def get_employee_by_id(self, id: UUID) -> Employee:
        """
        Retrieve an employee's identity information from the database using their database ID.

        Args:
            id: The database ID of the employee.
        Returns:
            The employee's identity information.
        """
        try:
            employee = self.session.exec(
                select(Employee).where(Employee.id == id)
            ).one()
            return employee
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee does not exist",
            )

    def delete_employee_by_id(self, id: UUID) -> Employee:
        """
        Delete an employee from the database using their database ID.

        Args:
            id: The database ID of the employee.
        Returns:
            The removed employee.
        """
        try:
            employee = self.session.exec(
                select(Employee).where(Employee.id == id)
            ).one()
            self.session.delete(employee)
            self.session.commit()
            return employee
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee does not exist",
            )


class EmployeeService(EmployeeServiceBase):
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

    def compute_email_code(self, employee: Employee) -> str:
        """
        Compute the email verification code for the given employee.
        Args:
            employee: The employee for which the code is to be computed.
        Returns:
            The computed email code.
        """
        state = self.get_employee_state(employee)
        prefix = state.code_to_print[-2:]
        suffix = state.code_to_print[-4:]
        email_code = prefix + hashlib.sha256(suffix.encode()).hexdigest()
        return email_code

    def generate_and_send_email(self, employee: Employee) -> EmployeeState:
        """
        Generates an email code for the given employee and sends it to their email address.
        Args:
            employee: The employee to whom the email is to be sent.
        """
        email_code = self.compute_email_code(employee)
        email_message = self.email_service.create_email(employee.email, email_code)
        self.email_service.send_email(email_message, employee.email)
        state = self.get_employee_state(employee)
        state.email_code_sent = True

        self.session.add(state)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update employee state",
            )
        return state

    def create_qr_code(self, employee: Employee) -> str:
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
        img = qrcode.make(employee.code_to_print)
        qr_code_path = f"app/static/qr_codes/{employee.internal_id}.png"
        img.save(qr_code_path)
        return qr_code_path

    def validate_email_code(self, employee: Employee, input_code: str) -> bool:
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
            self.session.add(state)
            try:
                self.session.commit()
            except IntegrityError:
                self.session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update employee state",
                )
            return True
        return False
