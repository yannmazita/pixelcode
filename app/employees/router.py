from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlmodel import Session
from app.auth.dependencies import validate_token
from app.auth.models import TokenData
from app.database import get_session
from app.emails.dependencies import get_email_service
from app.emails.services import EmailService
from app.employees.models import (
    EmployeeCreate,
    EmployeeIdentifier,
    EmployeeRead,
    EmployeeStateRead,
)
from app.employees.services import EmployeeAdminService, EmployeeService

router = APIRouter(
    prefix="/employees",
    tags=["employees"],
)


@router.post("/send-email", response_model=EmployeeStateRead)
async def send_verification_email(
    employee_identifier: EmployeeIdentifier,
    session: Annotated[Session, Depends(get_session)],
    email_service: Annotated[EmailService, Depends(get_email_service)],
):
    service = EmployeeService(session, email_service)
    if employee_identifier.internal_id:
        employee = service.get_employee_by_internal_id(employee_identifier.internal_id)
    else:
        employee = service.get_employee_by_email(employee_identifier.email)
    return service.generate_and_send_email(employee)


@router.post("/", response_model=EmployeeRead)
async def create_employee(
    employee: EmployeeCreate,
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    session: Annotated[Session, Depends(get_session)],
):
    admin_service = EmployeeAdminService(session)
    try:
        new_employee = admin_service.create_new_employee(employee)
        return new_employee
    except HTTPException as e:
        return e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
