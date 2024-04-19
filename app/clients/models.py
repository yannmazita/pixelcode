from pydantic import BaseModel

from app.auth.models import Token


class AppUpdate(BaseModel):
    email_exists: bool | None = None
    employee_id_exists: bool | None = None
    email_code_validated: bool = False


class AppEmployeeInformation(BaseModel):
    employee_id: str | None = None
    employee_email: str | None = None


class AppEmailCode(BaseModel):
    email_code: int


class AppError(BaseModel):
    error: str


class AppStats(BaseModel):
    active_users: int


class WebsocketMessage(BaseModel):
    action: str
    data: (
        Token
        | AppError
        | AppStats
        | AppUpdate
        | AppEmployeeInformation
        | AppEmailCode
        | None
    ) = None
