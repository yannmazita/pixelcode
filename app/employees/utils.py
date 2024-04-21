from uuid import uuid4
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from app.database import engine
from app.employees.models import Employee, EmployeeState


def add_fake_employee():
    employee = Employee(
        id=uuid4(),
        internal_id="12345",
        code_to_print="ABCDE",
        surname="Doe",
        firstname="John",
        email="john.doe@email.com",
    )
    db_employee = Employee.model_validate(employee)
    session = Session(engine)
    session.add(db_employee)
    try:
        session.commit()
    except IntegrityError:
        pass


def add_fake_employee_state():
    employee_state = EmployeeState(
        id=uuid4(),
        internal_id="12345",
        code_to_print="ABCDE",
        email_code_validated=False,
        email_code_sent=False,
    )
    db_employee_state = EmployeeState.model_validate(employee_state)
    session = Session(engine)
    session.add(db_employee_state)
    try:
        session.commit()
    except IntegrityError:
        pass
