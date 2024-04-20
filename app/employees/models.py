from pydantic import EmailStr, validate_call
from sqlmodel import SQLModel, Field
from uuid import UUID


class EmployeeIdentifier(SQLModel, table=False):
    employee_id: str | None = None
    employee_email: EmailStr | None = None

    @validate_call
    def __init__(self, **data):
        super().__init__(**data)
        if not self.employee_id and not self.employee_email:
            raise ValueError("Either employee_id or employee_email must be provided")
        if self.employee_id and self.employee_email:
            raise ValueError(
                "Only one of employee_id or employee_email should be provided"
            )


class EmployeeIdentity(SQLModel, table=True):
    id: UUID | None = Field(default=None, primary_key=True)
    employee_id: str  # Unique employee id
    employee_code: str  # Unique code which will be printed
    surname: str
    firstname: str
    employee_email: str


class EmployeeState(SQLModel, table=True):
    id: UUID | None = Field(
        default=None, primary_key=True, foreign_key="employeeidentity.id"
    )
    employee_code_in_database: str = Field(
        default=None, foreign_key="employeeidentity.employee_code"
    )
    email_code_validated: bool = False
    email_code_sent: bool = False
