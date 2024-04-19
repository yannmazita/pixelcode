from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlmodel import Field, Session, SQLModel

from .database import engine


class Token(BaseModel):
    access_token: str | None
    token_type: str | None


class TokenData(SQLModel):
    username: str | None = None
    scopes: list[str] = []


class AppUpdate(BaseModel):
    email_exists: bool | None = None
    employee_id_exists: bool | None = None
    email_code_validated: bool = False


class AppEmployeeInformation(BaseModel):
    employee_id: str | None = None
    employee_email: str | None = None


class AppError(BaseModel):
    error: str


class AppStats(BaseModel):
    active_users: int


class WebsocketMessage(BaseModel):
    action: str
    data: Token | AppError | AppStats | AppUpdate | None = None


class UserBase(SQLModel):
    username: str = Field(unique=True)
    employee_id: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    firstname: str | None = Field(default=None)
    surname: str | None = Field(default=None)


class User(UserBase, table=True):
    id: UUID | None = Field(default=None, primary_key=True)
    employee_code: str = Field(index=True, unique=True)
    roles: str = Field(default="user.create user:own user:own.write")


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: UUID


def create_fake_users():
    user1: User = User(
        id=uuid4(),
        username="user",
        employee_id="12345",
        email="email@email.com",
        employee_code="fakec0d3",
    )
    user2: User = User(
        id=uuid4(),
        username="user2",
        employee_id="54321",
        email="email2@email.com",
        employee_code="fakec0d32",
    )
    db_user1 = User.model_validate(user1)
    db_user2 = User.model_validate(user2)
    session = Session(engine)
    session.add(db_user1)
    session.add(db_user2)
    try:
        session.commit()
    except IntegrityError:
        pass


def create_admin_user():
    user: User = User(
        id=uuid4(),
        username="admin",
        employee_id="admin",
        email="admin@admin.com",
        employee_code="admin",
        roles="admin",
    )
    db_user = User.model_validate(user)
    session = Session(engine)
    session.add(db_user)
    try:
        session.commit()
    except IntegrityError:
        pass
