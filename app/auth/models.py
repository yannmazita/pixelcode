from pydantic import BaseModel
from sqlmodel import SQLModel


class Token(BaseModel):
    access_token: str | None
    token_type: str | None


class TokenData(SQLModel):
    username: str | None = None
    scopes: list[str] = []
