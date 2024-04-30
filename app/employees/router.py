from typing import Annotated
from uuid import UUID
from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    HTTPException,
    Security,
    status,
)
from pydantic import EmailStr
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
from app.employees.schemas import EmployeeAttribute, EmployeeStateAttribute
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
        employee = service.get_employee_by_attribute(
            EmployeeAttribute.INTERNAL_ID, employee_identifier.internal_id
        )
    else:
        employee = service.get_employee_by_attribute(
            EmployeeAttribute.EMAIL, str(employee_identifier.email)
        )
    return service.generate_and_send_email(employee)


@router.post("/upload-csv")
async def upload_csv(
    file: UploadFile,
    session: Annotated[Session, Depends(get_session)],
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
):
    admin_service = EmployeeAdminService(session)
    employees = await admin_service.parse_csv_file(file)

    try:
        for employee in employees:
            # implement batch processing instead, this is slow
            admin_service.create_new_employee(employee)
    except HTTPException as e:
        session.rollback()
        raise e
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


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
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/id/{id}", response_model=EmployeeRead)
async def get_employee_by_id(
    id: UUID,
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    session: Annotated[Session, Depends(get_session)],
):
    admin_service = EmployeeAdminService(session)
    try:
        employee = admin_service.get_employee_by_attribute(
            EmployeeAttribute.ID, str(id)
        )
        return employee
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/internal_id/{internal_id}", response_model=EmployeeRead)
async def get_employee_by_internal_id(
    internal_id: str,
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    session: Annotated[Session, Depends(get_session)],
):
    admin_service = EmployeeAdminService(session)
    try:
        employee = admin_service.get_employee_by_attribute(
            EmployeeAttribute.INTERNAL_ID, internal_id
        )
        return employee
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/email/{email}", response_model=EmployeeRead)
async def get_employee_by_email(
    email: EmailStr,
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    session: Annotated[Session, Depends(get_session)],
):
    admin_service = EmployeeAdminService(session)
    try:
        employee = admin_service.get_employee_by_attribute(
            EmployeeAttribute.EMAIL, email
        )
        return employee
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/all", response_model=list[EmployeeRead])
async def get_all_employees(
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    session: Annotated[Session, Depends(get_session)],
):
    admin_service = EmployeeAdminService(session)
    try:
        employees = admin_service.get_employees()
        return employees
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.put("/id/{id}", response_model=EmployeeRead)
async def update_employee_by_id(
    id: UUID,
    employee: EmployeeCreate,
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    session: Annotated[Session, Depends(get_session)],
):
    admin_service = EmployeeAdminService(session)
    try:
        updated_employee = admin_service.update_employee_by_attribute(
            EmployeeAttribute.ID, str(id), employee
        )
        return updated_employee
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.put("/internal_id/{internal_id}", response_model=EmployeeRead)
async def update_employee_by_internal_id(
    internal_id: str,
    employee: EmployeeCreate,
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    session: Annotated[Session, Depends(get_session)],
):
    admin_service = EmployeeAdminService(session)
    try:
        updated_employee = admin_service.update_employee_by_attribute(
            EmployeeAttribute.INTERNAL_ID, internal_id, employee
        )
        return updated_employee
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.put("/email/{email}", response_model=EmployeeRead)
async def update_employee_by_email(
    email: EmailStr,
    employee: EmployeeCreate,
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    session: Annotated[Session, Depends(get_session)],
):
    admin_service = EmployeeAdminService(session)
    try:
        updated_employee = admin_service.update_employee_by_attribute(
            EmployeeAttribute.EMAIL, email, employee
        )
        return updated_employee
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete("/id/{id}", response_model=EmployeeRead)
async def delete_employee_by_id(
    id: UUID,
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    session: Annotated[Session, Depends(get_session)],
):
    admin_service = EmployeeAdminService(session)
    try:
        employee = admin_service.delete_employee_by_attribute(
            EmployeeAttribute.ID, str(id)
        )
        return employee
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete("/internal_id/{internal_id}", response_model=EmployeeRead)
async def delete_employee_by_internal_id(
    internal_id: str,
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    session: Annotated[Session, Depends(get_session)],
):
    admin_service = EmployeeAdminService(session)
    try:
        employee = admin_service.delete_employee_by_attribute(
            EmployeeAttribute.INTERNAL_ID, internal_id
        )
        return employee
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete("/email/{email}", response_model=EmployeeRead)
async def delete_employee_by_email(
    email: EmailStr,
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    session: Annotated[Session, Depends(get_session)],
):
    admin_service = EmployeeAdminService(session)
    try:
        employee = admin_service.delete_employee_by_attribute(
            EmployeeAttribute.EMAIL, email
        )
        return employee
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/state/id/{id}", response_model=EmployeeStateRead)
async def get_employee_state_by_id(
    id: UUID,
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    session: Annotated[Session, Depends(get_session)],
):
    admin_service = EmployeeAdminService(session)
    try:
        employee_state = admin_service.get_employee_state_by_attribute(
            EmployeeStateAttribute.ID, str(id)
        )
        return employee_state
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/state/all", response_model=list[EmployeeStateRead])
async def get_all_employee_states(
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    session: Annotated[Session, Depends(get_session)],
):
    admin_service = EmployeeAdminService(session)
    try:
        employee_states = admin_service.get_employee_states()
        return employee_states
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete("/state/id/{id}", response_model=EmployeeStateRead)
async def delete_employee_state_by_id(
    id: UUID,
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    session: Annotated[Session, Depends(get_session)],
):
    admin_service = EmployeeAdminService(session)
    try:
        employee_state = admin_service.delete_employee_state_by_attribute(
            EmployeeStateAttribute.ID, str(id)
        )
        return employee_state
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
