from fastapi import Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.employees.models import EmployeeIdentifier, Employee
from app.employees.services import EmployeeService
from app.emails.services import EmailService
from app.emails.dependencies import get_email_service


def get_employee_from_identifier(
    identifier: EmployeeIdentifier,
    session: Session = Depends(get_session),
    email_service: EmailService = Depends(get_email_service),
) -> Employee:
    service = EmployeeService(session=session, email_service=email_service)
    if identifier.internal_id:
        return service.get_employee_by_internal_id(identifier.internal_id)
    elif identifier.email:
        return service.get_employee_by_email(identifier.email)
    else:
        raise HTTPException(status_code=400, detail="Invalid identifier provided")
