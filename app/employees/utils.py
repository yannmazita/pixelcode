from uuid import UUID
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from app.database import engine
from app.employees.models import EmployeeIdentity, EmployeeState


def add_fake_employee():
    employee = EmployeeIdentity(
        id=UUID("123e4567-e89b-12d3-a456-426614174000", version=4),
        employee_id="12345",
        employee_code="ABCDE",
        surname="Doe",
        firstname="John",
        employee_email="john.doe@email.com",
    )
    db_employee = EmployeeIdentity.model_validate(employee)
    session = Session(engine)
    session.add(db_employee)
    try:
        session.commit()
    except IntegrityError:
        pass


def add_fake_employee_state():
    employee_state = EmployeeState(
        id=UUID("123e4567-e89b-12d3-a456-426614174000", version=4),
        employee_code_in_database="ABCDE",
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
