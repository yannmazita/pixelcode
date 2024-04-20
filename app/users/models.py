from uuid import UUID
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)


class User(UserBase, table=True):
    id: UUID | None = Field(default=None, primary_key=True)
    hashed_password: str
    roles: str = Field(default="user.create user:own user:own.write websockets")


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: UUID
