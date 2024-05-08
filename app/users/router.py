from typing import Annotated
from uuid import UUID
from fastapi import Depends, APIRouter, HTTPException, Security, status
from sqlmodel import Session
from app.database import get_session
from app.auth.dependencies import validate_token
from app.auth.models import TokenData
from app.users.dependencies import get_own_user
from app.users.models import (
    User,
    UserCreate,
    UserPasswordUpdate,
    UserRead,
    UserRolesUpdate,
    UserUsernameUpdate,
)
from app.users.services import UserService, UserAdminService
from app.users.schemas import UserAttribute

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", response_model=UserRead)
async def create_user(
    user: UserCreate,
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    session: Session = Depends(get_session),
):
    service = UserService(session)
    try:
        new_user = service.create_user(user)
        return new_user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/id/{id}", response_model=UserRead)
async def get_user_by_id(
    id: UUID,
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    session: Annotated[Session, Depends(get_session)],
):
    service = UserService(session)
    try:
        user = service.get_user_by_attribute(UserAttribute.ID, str(id))
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/all", response_model=tuple[list[UserRead], int])
async def get_all_users(
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    session: Annotated[Session, Depends(get_session)],
    offset: int = 0,
    limit: int = 100,
):
    service = UserService(session)
    try:
        users, total_count = service.get_users(offset, limit)
        print(total_count)
        return users, total_count
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.put("/id/{id}", response_model=UserRead)
async def update_user_by_id(
    id: UUID,
    user: UserCreate,
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    session: Annotated[Session, Depends(get_session)],
):
    service = UserService(session)
    try:
        updated_user = service.update_user_by_attribute(UserAttribute.ID, str(id), user)
        return updated_user
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete("/id/{id}", response_model=UserRead)
async def delete_user_by_id(
    id: UUID,
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    session: Annotated[Session, Depends(get_session)],
):
    service = UserService(session)
    try:
        user = service.delete_user_by_attribute(UserAttribute.ID, str(id))
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.patch("/id/{id}/username", response_model=UserRead)
async def update_user_username_by_id(
    id: UUID,
    username_data: UserUsernameUpdate,
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    session: Annotated[Session, Depends(get_session)],
):
    admin_service = UserAdminService(session)
    try:
        updated_user = admin_service.update_user_username_by_attribute(
            UserAttribute.ID, str(id), username_data
        )
        return updated_user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.patch("/id/{id}/roles", response_model=UserRead)
async def update_user_roles_by_id(
    id: UUID,
    roles_data: UserRolesUpdate,
    token_data: Annotated[TokenData, Security(validate_token, scopes=["admin"])],
    session: Annotated[Session, Depends(get_session)],
):
    admin_service = UserAdminService(session)
    try:
        updated_user = admin_service.update_user_roles_by_attribute(
            UserAttribute.ID, str(id), roles_data
        )
        return updated_user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/me", response_model=UserRead)
async def get_own_user(user: Annotated[User, Depends(get_own_user)]):
    return user


@router.delete("/me", response_model=UserRead)
async def delete_own_user(
    user: Annotated[User, Depends(get_own_user)],
    session: Annotated[Session, Depends(get_session)],
):
    service = UserService(session)
    try:
        service.delete_user(user)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    return user


@router.patch("/me/password", response_model=UserRead)
async def update_own_password(
    user: Annotated[User, Depends(get_own_user)],
    password_data: UserPasswordUpdate,
    session: Annotated[Session, Depends(get_session)],
):
    service = UserService(session)
    try:
        service.update_user_password(user, password_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    return user
