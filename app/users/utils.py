from sqlmodel import Session
from app.database import engine
from app.users.services import UserService, UserAdminService
from app.users.models import UserCreate
from app.users.schemas import UserAttribute


def create_superuser():
    session: Session = Session(engine)
    service = UserService(session)
    admin_user: UserCreate = UserCreate(
        username="admin",
        password="secret",
    )
    service.create_user(admin_user)

    admin_service = UserAdminService(session)
    admin_service.update_user_roles_by_attribute(
        UserAttribute.USERNAME, "admin", "admin"
    )
