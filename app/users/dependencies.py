from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Query, Security, status
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from app.auth.services import get_password_hash
from app.database import engine
from app.auth.dependencies import validate_token
from app.dependencies import get_user_by_username
from app.auth.models import TokenData
from app.users.models import User, UserCreate


async def get_own_user(
    token_data: Annotated[TokenData, Security(validate_token, scopes=["user:own"])],
) -> User:
    """Get own user.
    Args:
        token_data: Token data.
    Returns:
        A User instance representing own user.
    """
    assert token_data.username is not None
    user: User = await get_user_by_username(token_data.username)

    if user.banned:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Banned user"
        )
    return user


async def create_new_user(
    token_data: Annotated[TokenData, Security(validate_token, scopes=["user.create"])],
    user: UserCreate,
) -> User:
    """Create new user.
    Args:
        token_data: Token data.
        user: User to create.
    Returns:
        A User instance representing the created user.
    """
    if token_data.username != user.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username in token and body do not match",
        )

    with Session(engine) as session:
        try:
            # Should not be possible, but better be bulletproof.
            session.exec(select(User).where(User.username == user.username)).one()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this username already exists",
            )
        except NoResultFound:
            pass
    hashed_password: str = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db_user = User.model_validate(new_user)
    with Session(engine) as session:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    return db_user


async def get_users(
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    with Session(engine) as session:
        users = session.exec(select(User).offset(offset).limit(limit)).all()
        return users


async def get_user_by_id(user_id: UUID) -> User:
    with Session(engine) as session:
        try:
            user = session.exec(select(User).where(User.id == user_id)).one()
            return user
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
            )


async def get_user(
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    user_id: UUID,
) -> User:
    return await get_user_by_id(user_id)


async def remove_user_by_id(user_id: UUID) -> User:
    with Session(engine) as session:
        try:
            user = session.exec(select(User).where(User.id == user_id)).one()
            session.delete(user)
            session.commit()
            return user
        except AttributeError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
            )


async def remove_user(
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    user_id: UUID,
) -> User:
    return await remove_user_by_id(user_id)


async def remove_own_user(user: Annotated[User, Depends(get_own_user)]) -> User:
    assert user.id is not None
    return await remove_user_by_id(user.id)
