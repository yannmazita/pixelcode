import os
from uuid import uuid4
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from app.database import get_session
from app.users.services import UserService
from app.users.models import User, UserCreate
from app.database import engine

SUPER_PASSWORD: str = os.getenv("SUPERUSER_PASSWORD")  # type: ignore


def create_superuser():
    pass
