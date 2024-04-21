from pydantic import EmailStr, validate_call
from sqlmodel import SQLModel, Field, String
from uuid import UUID


class EmployeeBase(SQLModel):
    internal_id: str = Field(index=True, unique=True)
    email: EmailStr = Field(sa_type=String(), index=True, unique=True)


class Employee(EmployeeBase, table=True):
    id: UUID | None = Field(default=None, primary_key=True)
    code_to_print: str = Field(unique=True)  # Unique code which will be printed
    surname: str
    firstname: str


class EmployeeCreate(EmployeeBase):
    code_to_print: str
    surname: str
    firstname: str


class EmployeeRead(EmployeeBase):
    id: UUID
    code_to_print: str
    surname: str
    firstname: str


class EmployeeStateBase(SQLModel):
    internal_id: str = Field(index=True, foreign_key="employee.internal_id")
    code_to_print: str = Field(foreign_key="employee.code_to_print")
    email_code_validated: bool = False
    email_code_sent: bool = False


class EmployeeState(EmployeeStateBase, table=True):
    id: UUID | None = Field(default=None, primary_key=True)


class EmployeeStateRead(EmployeeStateBase):
    pass


class EmployeeIdentifier(SQLModel, table=False):
    internal_id: str | None = None
    email: EmailStr | None = None

    @validate_call
    def __init__(self, **data):
        super().__init__(**data)
        if not self.internal_id and not self.email:
            raise ValueError("Either internal_id or email must be provided")
        if self.internal_id and self.email:
            raise ValueError("Only one of internal_id or email should be provided")
