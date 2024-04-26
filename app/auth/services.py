import os
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from jose import jwt
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from app.auth.exceptions import incorrect_username_or_password
from app.database import engine
from app.users.exceptions import user_not_found
from app.users.models import User


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    try:
        session: Session = Session(engine)
        user = session.exec(select(User).where(User.username == username)).one()
    except NoResultFound:
        raise user_not_found
    if not verify_password(password, user.hashed_password):
        raise incorrect_username_or_password
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # type: ignore
    return encoded_jwt
