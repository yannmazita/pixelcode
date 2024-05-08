from fastapi import HTTPException
from sqlmodel import Session
from app.database import engine
from app.users.services import UserService, UserAdminService
from app.users.models import UserCreate, UserRolesUpdate
from app.users.schemas import UserAttribute


def create_superuser():
    session: Session = Session(engine)
    service = UserService(session)
    admin_user: UserCreate = UserCreate(
        username="admin",
        password="secret",
    )
    try:
        service.create_user(admin_user)
    except HTTPException as e:
        pass

    admin_service = UserAdminService(session)
    admin_service.update_user_roles_by_attribute(
        UserAttribute.USERNAME, "admin", UserRolesUpdate(roles="admin")
    )


def create_fake_users():
    session: Session = Session(engine)
    service = UserService(session)
    for i in range(150):
        user: UserCreate = UserCreate(
            username=f"fake_user_{i}",
            password="secret",
        )
        try:
            service.create_user(user)
        except HTTPException as e:
            pass
        if i % 2 == 0:
            admin_service = UserAdminService(session)
            admin_service.update_user_roles_by_attribute(
                UserAttribute.USERNAME,
                f"fake_user_{i}",
                UserRolesUpdate(roles="user:own websockets"),
            )
