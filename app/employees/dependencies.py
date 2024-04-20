from fastapi import Depends, HTTPException
from sqlmodel import Session
from app.auth.services import get_password_hash
from app.auth.models import TokenData
from app.database import get_session
from app.employees.models import EmployeeIdentifier, EmployeeIdentity
from app.employees.services import EmployeeService
from app.emails.services import EmailService
from app.emails.dependencies import get_email_service


def get_employee_from_identifier(
    identifier: EmployeeIdentifier,
    session: Session = Depends(get_session),
    email_service: EmailService = Depends(get_email_service),
) -> EmployeeIdentity:
    service = EmployeeService(session=session, email_service=email_service)
    if identifier.employee_id:
        return service.get_employee_identity_by_employee_id(identifier.employee_id)
    elif identifier.employee_email:
        return service.get_employee_identity_by_email(identifier.employee_email)
    else:
        raise HTTPException(status_code=400, detail="Invalid identifier provided")
