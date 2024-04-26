from fastapi import HTTPException, status
from uuid import uuid4, UUID
from sqlmodel import Session, select
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from app.auth.services import get_password_hash
from app.users.exceptions import (
    user_not_found,
    multiple_users_found,
    user_already_exists,
)
from app.users.models import User, UserCreate
from app.users.schemas import UserAttribute


class UserServiceBase:
    """
    Base class for user-related operations.

    Attributes:
        session: The database session to be used for operations.
    """

    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: UserCreate) -> User:
        """
        Create a new user.
        Args:
            user: The user data.
        Returns:
            The created user.
        """
        try:
            self.session.exec(select(User).where(User.username == user.username)).one()
            raise user_already_exists
        except NoResultFound:
            pass

        hashed_password = get_password_hash(user.password)
        new_user = User(
            id=uuid4(), username=user.username, hashed_password=hashed_password
        )
        db_user = User.model_validate(new_user)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)

        return db_user

    def get_user_by_attribute(self, attribute: UserAttribute, value: str) -> User:
        """
        Get a user by a specified attribute.
        Args:
            attribute: The attribute to filter by.
            value: The value to filter by.
        Returns:
            The user with the specified attribute and value.
        """
        try:
            user = self.session.exec(
                select(User).where(getattr(User, attribute.value) == value)
            ).one()
        except MultipleResultsFound:
            raise multiple_users_found
        except NoResultFound:
            raise user_not_found
        return user

    def update_user_by_attribute(
        self, attribute: UserAttribute, value: str, user: UserCreate
    ) -> User:
        """
        Update a user using a specified attribute.
        Args:
            attribute: The attribute to filter by.
            value: The value to filter by.
            user: The new user data.
        Returns:
            The updated user.
        """
        try:
            user_db = self.get_user_by_attribute(attribute, value)
            user_data = user.model_dump()
            for key, value in user_data.items():
                setattr(user_db, key, value)
            self.session.add(user_db)
            self.session.commit()
            return user_db
        except NoResultFound:
            raise user_not_found
        except MultipleResultsFound:
            raise multiple_users_found

    def delete_user(self, user: User) -> User:
        """
        Delete a user.
        Args:
            user: The user to delete.
        Returns:
            The deleted user.
        """
        try:
            self.session.delete(user)
            self.session.commit()
        except NoResultFound:
            raise user_not_found
        return user

    def delete_user_by_attribute(self, attribute: UserAttribute, value: str) -> User:
        """
        Delete a user using a specified attribute.
        Args:
            attribute: The attribute to filter by.
            value: The value to filter by.
        Returns:
            The deleted user.
        """
        try:
            user = self.get_user_by_attribute(attribute, value)
            self.session.delete(user)
            self.session.commit()
            return user
        except NoResultFound:
            raise user_not_found
        except MultipleResultsFound:
            raise multiple_users_found

    def get_users(self, offset: int = 0, limit: int = 100):
        """
        Get all users.
        Args:
            offset: The number of users to skip.
            limit: The maximum number of users to return.
        Returns:
            The list of users.
        """
        users = self.session.exec(select(User).offset(offset).limit(limit)).all()
        return users


class UserService(UserServiceBase):
    """
    Class for user-related operations.
    Attributes:
        session: The database session to be used for operations.
    """

    def __init__(self, session: Session):
        super().__init__(session)


class UserAdminService(UserServiceBase):
    """
    Class for user-related operations.
    Attributes:
        session: The database session to be used for operations.
    """

    def __init__(self, session: Session):
        super().__init__(session)

    def update_user_roles_by_attribute(
        self, attribute: UserAttribute, value: str, new_roles: str
    ) -> User:
        """
        Update a user's roles using a specified attribute.
        Args:
            attribute: The attribute to filter by.
            value: The value to filter by.
            new_roles: The new roles.
        Returns:
            The updated user.
        """
        try:
            user = self.get_user_by_attribute(attribute, value)
            user.roles = new_roles
            self.session.add(user)
            self.session.commit()
            return user
        except NoResultFound:
            raise user_not_found
        except MultipleResultsFound:
            raise multiple_users_found
