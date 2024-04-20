from typing import Annotated
from fastapi import APIRouter, Depends
from app.database import get_session
from app.emails.dependencies import get_email_service
from app.employees.dependencies import get_employee_from_identifier
from app.employees.models import EmployeeIdentifier
from app.employees.services import EmployeeService

router = APIRouter(
    prefix="/employees",
    tags=["employees"],
)

@router.post("/send-email")
async def send_verification_email(employee_identifier: Annotated[EmployeeIdentifier, Depends()]):
    employee = get_employee_from_identifier(employee_identifier)
    service = EmployeeService(
        session=Depends(get_session), email_service=Depends(get_email_service)
    )
    service.generate_and_send_email(employee)
    return {"message": "Email sent successfully"}
