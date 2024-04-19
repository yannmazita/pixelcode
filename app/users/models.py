from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlmodel import Field, Session, SQLModel

from app.database import engine


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)


class User(UserBase, table=True):
    id: UUID | None = Field(default=None, primary_key=True)
    hashed_password: str
    banned: bool = Field(default=False)
    roles: str = Field(default="user.create user:own user:own.write websockets")


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: UUID


def create_fake_users():
    user1: User = User(
        id=uuid4(),
        username="user1",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
    )
    user2: User = User(
        id=uuid4(),
        username="user2",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
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
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        roles="admin",
    )
    db_user = User.model_validate(user)
    session = Session(engine)
    session.add(db_user)
    try:
        session.commit()
    except IntegrityError:
        pass
