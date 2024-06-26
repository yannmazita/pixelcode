import csv
import hashlib
from io import TextIOWrapper
from pathlib import Path
from fastapi import HTTPException, UploadFile, status
import qrcode
from uuid import UUID, uuid4
from sqlmodel import Session, select
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from app.employees.models import (
    Employee,
    EmployeeCreate,
    EmployeeState,
)
from app.employees.schemas import EmployeeAttribute, EmployeeStateAttribute
from app.emails.services import EmailService


class EmployeeServiceBase:
    """
    Base class for employee-related operations.

    This class provides methods to interact with the database and perform operations on employees.
    It is intended to be used by other service classes.

    Attributes:
        session: The database session to be used for operations.
    """

    def __init__(self, session: Session):
        self.session = session

    def get_employee_by_attribute(
        self, attribute: EmployeeAttribute, value: str
    ) -> Employee:
        """
        Retrieve an employee's identity information from the database using an attribute.
        Args:
            attribute: The attribute to be used for retrieval.
            value: The value of the attribute.
        Returns:
            The employee's identity information.
        """
        try:
            employee = self.session.exec(
                select(Employee).where(getattr(Employee, attribute.value) == value)
            ).one()
            return employee
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with {attribute.value} = {value} does not exist",
            )
        except MultipleResultsFound:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Multiple employees found with {attribute.value} = {value}",
            )

    def update_employee_by_attribute(
        self, attribute: EmployeeAttribute, value: str, employee: EmployeeCreate
    ) -> Employee:
        """
        Update an employee's information in the database using an attribute.
        Args:
            attribute: The attribute to be used for retrieval.
            value: The value of the attribute.
            employee: The updated employee information.
        Returns:
            The updated employee.
        """
        try:
            db_employee = self.session.exec(
                select(Employee).where(getattr(Employee, attribute.value) == value)
            ).one()
            db_employee.internal_id = employee.internal_id
            db_employee.email = employee.email
            db_employee.code_to_print = employee.code_to_print
            db_employee.surname = employee.surname
            db_employee.firstname = employee.firstname
            self.session.add(db_employee)
            self.session.commit()
            self.session.refresh(db_employee)
            return db_employee
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with {attribute.value} = {value} does not exist",
            )
        except MultipleResultsFound:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Multiple employees found with {attribute.value} = {value}",
            )

    def delete_employee_by_attribute(
        self, attribute: EmployeeAttribute, value: str
    ) -> Employee:
        """
        Delete an employee from the database using an attribute.
        Args:
            attribute: The attribute to be used for retrieval.
            value: The value of the attribute.
        Returns:
            The removed employee.
        """
        try:
            employee = self.session.exec(
                select(Employee).where(getattr(Employee, attribute.value) == value)
            ).one()
            self.session.delete(employee)
            self.session.commit()
            return employee
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with {attribute.value} = {value} does not exist",
            )
        except MultipleResultsFound:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Multiple employees found with {attribute.value} = {value}",
            )

    def create_employee_state(self, employee: Employee) -> EmployeeState:
        """
        Create a new employee state in the database.

        Args:
            employee: The employee for whom the state is to be created.
        Returns:
            The created employee state.
        """
        try:
            self.session.exec(
                select(EmployeeState).where(
                    EmployeeState.internal_id == employee.internal_id
                )
            ).one()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="State for employee already exists",
            )
        except NoResultFound:
            pass
        new_state = EmployeeState(
            internal_id=employee.internal_id,
            code_to_print=employee.code_to_print,
        )
        db_state = EmployeeState.model_validate(new_state)
        self.session.add(db_state)
        self.session.commit()
        self.session.refresh(db_state)
        return db_state

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
        except MultipleResultsFound:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Multiple states found for employee",
            )

    def update_employee_state(
        self, employee: Employee, state: EmployeeState
    ) -> EmployeeState:
        """
        Update an employee's state information in the database.
        Args:
            employee: The employee whose state information is to be updated.
            state: The updated state information.
        Returns:
            The updated state information.
        """
        try:
            db_state = self.session.exec(
                select(EmployeeState).where(
                    EmployeeState.internal_id == employee.internal_id
                )
            ).one()
            db_state.email_code_validated = state.email_code_validated
            db_state.email_code_sent = state.email_code_sent
            self.session.add(db_state)
            self.session.commit()
            self.session.refresh(db_state)
            return db_state
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee state does not exist",
            )
        except MultipleResultsFound:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Multiple states found for employee",
            )

    def ensure_employee_state(self, employee: Employee) -> EmployeeState:
        """
        Ensure that an employee state exists in the database.

        This method checks if an employee state exists in the database, and creates one if it does not.
        Args:
            employee: The employee for whom the state is to be ensured.
        Returns:
            The employee state.
        """
        try:
            state = self.get_employee_state(employee)
        except HTTPException as e:
            if e.status_code == status.HTTP_404_NOT_FOUND:
                state = self.create_employee_state(employee)
            else:
                raise e
        return state


class EmployeeAdminService(EmployeeServiceBase):
    """
    Service class for employee-related operations.

    This class provides methods to interact with the database and perform operations on employees.
    It is intended to be used by administrators.
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
        self.session.refresh(db_employee)

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

    def get_employee_state_by_attribute(
        self, attribute: EmployeeStateAttribute, value: str
    ) -> EmployeeState:
        """
        Retrieve an employee's state information from the database using an attribute.

        Args:
            attribute: The attribute to be used for retrieval.
            value: The value of the attribute.
        Returns:
            The employee's state information.
        """
        try:
            state = self.session.exec(
                select(EmployeeState).where(
                    getattr(EmployeeState, attribute.value) == value
                )
            ).one()
            return state
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee state with {attribute.value} = {value} does not exist",
            )
        except MultipleResultsFound:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Multiple states found with {attribute.value} = {value}",
            )

    def update_employee_state_by_attribute(
        self, attribute: EmployeeStateAttribute, value: str, state: EmployeeState
    ) -> EmployeeState:
        """
        Update an employee's state information in the database using an attribute.

        Args:
            attribute: The attribute to be used for retrieval.
            value: The value of the attribute.
            state: The updated state information.
        Returns:
            The updated state information.
        """
        try:
            db_state = self.session.exec(
                select(EmployeeState).where(
                    getattr(EmployeeState, attribute.value) == value
                )
            ).one()
            db_state.email_code_validated = state.email_code_validated
            db_state.email_code_sent = state.email_code_sent
            self.session.add(db_state)
            self.session.commit()
            self.session.refresh(db_state)
            return db_state
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee state with {attribute.value} = {value} does not exist",
            )
        except MultipleResultsFound:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Multiple states found with {attribute.value} = {value}",
            )

    def delete_employee_state_by_attribute(
        self, attribute: EmployeeStateAttribute, value: str
    ) -> EmployeeState:
        """
        Delete an employee state from the database using an attribute.

        Args:
            attribute: The attribute to be used for retrieval.
            value: The value of the attribute.
        Returns:
            The removed employee state.
        """
        try:
            state = self.session.exec(
                select(EmployeeState).where(
                    getattr(EmployeeState, attribute.value) == value
                )
            ).one()
            self.session.delete(state)
            self.session.commit()
            return state
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee state with {attribute.value} = {value} does not exist",
            )
        except MultipleResultsFound:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Multiple states found with {attribute.value} = {value}",
            )

    def get_employee_states(self, offset: int = 0, limit: int = 100):
        """
        Retrieve a list of employee states from the database.
        Args:
            offset: The number of records to skip.
            limit: The maximum number of records to return.
        Returns:
            A list of employee states.
        """

        states = self.session.exec(
            select(EmployeeState).offset(offset).limit(limit)
        ).all()
        return states

    ######## danger #######
    async def parse_csv_file(self, file: UploadFile) -> list[EmployeeCreate]:
        """
        Parse a CSV file containing employee information.
        Args:
            file: The CSV file to be parsed.
        Returns:
            A list of employee information.
        """
        employees = []
        # Read the content as a string stream directly
        contents = await file.read()
        # Decode to string if necessary
        content_string = contents.decode("utf-8")
        reader = csv.DictReader(content_string.splitlines())
        for row in reader:
            employee = EmployeeCreate(
                internal_id=row["internal_id"],
                email=row["email"],
                code_to_print=row["code_to_print"],
                surname=row["surname"],
                firstname=row["firstname"],
            )
            employees.append(employee)
        await file.close()
        return employees


class EmployeeService(EmployeeServiceBase):
    """
    Service class for employee-related operations.

    This class provides methods to interact with the database and perform operations on employees.
    It is intended to be used by employees themselves.

    Attributes:
        email_service: The email service to be used for sending emails.
    """

    def __init__(self, session: Session, email_service: EmailService):
        super().__init__(session)
        self.email_service = email_service

    def compute_email_code(self, employee: Employee) -> str:
        """
        Compute the email verification code for the given employee.
        Args:
            employee: The employee for which the code is to be computed.
        Returns:
            The computed email code.
        """
        prefix = employee.internal_id[-2:]
        email_code = (
            prefix + hashlib.md5(employee.internal_id.encode()).hexdigest()[-4:]
        )
        return email_code

    def generate_and_send_email(self, employee: Employee) -> EmployeeState:
        """
        Generates an email code for the given employee and sends it to their email address.
        Args:
            employee: The employee to whom the email is to be sent.
        """
        email_code = self.compute_email_code(employee)
        email_message = self.email_service.create_email(employee.email, email_code)
        state = self.ensure_employee_state(employee)

        try:
            self.email_service.send_email(email_message, employee.email)
            state.email_code_sent = True
        except Exception as e:
            # Very crude, needs to be more thorough
            print(e)
            state.email_code_sent = False

        self.update_employee_state(employee, state)
        return state

    def create_qr_code(self, employee: Employee) -> str:
        """
        Creates a QR code for the given employee.
        Args:
            employee: The employee for whom the QR code is to be created.
        Returns:
            The path to the created QR code.
        """
        state = self.ensure_employee_state(employee)
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
        state = self.ensure_employee_state(employee)
        if input_code == expected_code:
            state.email_code_validated = True
            self.update_employee_state(employee, state)
            return True
        return False
