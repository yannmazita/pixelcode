from uuid import UUID
from pydantic import validate_call
from sqlmodel import Field, SQLModel
from app.auth.config import OAUTH_SCOPES


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)


class User(UserBase, table=True):
    id: UUID | None = Field(default=None, primary_key=True)
    hashed_password: str
    roles: str = Field(default="")


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: UUID
    roles: str


class UserRolesUpdate(SQLModel, table=False):
    roles: str

    @validate_call
    def __init__(self, **data):
        super().__init__(**data)
        self.validate_roles()

    def validate_roles(self):
        valid_roles = set(OAUTH_SCOPES.keys())
        given_roles = set(self.roles.split())
        print(f"{'#'*10} given_roles={given_roles}")
        if not given_roles.issubset(valid_roles):
            raise ValueError(f"Invalid roles: {given_roles - valid_roles}")
