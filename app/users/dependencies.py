from typing import Annotated
from fastapi import Depends, Security
from sqlmodel import Session
from app.auth.dependencies import validate_token
from app.auth.models import TokenData
from app.database import get_session
from app.users.models import User
from app.users.services import UserService
from app.users.schemas import UserAttribute


async def get_own_user(
    token_data: Annotated[TokenData, Security(validate_token, scopes=["user:own"])],
    session: Annotated[Session, Depends(get_session)],
) -> User:
    """Get own user.
    Args:
        token_data: Token data.
    Returns:
        A User instance representing own user.
    """
    service = UserService(session)
    assert token_data.username is not None
    user: User = service.get_user_by_attribute(
        UserAttribute.USERNAME, token_data.username
    )

    return user
