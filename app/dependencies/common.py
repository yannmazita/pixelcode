from fastapi import HTTPException, status
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound

from app.database import engine
from app.models import User


async def get_user_by_username(username: str) -> User:
    with Session(engine) as session:
        try:
            user = session.exec(select(User).where(User.username == username)).one()
            return user
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
            )
