from typing import Annotated

from fastapi import Depends, APIRouter

from app.users.dependencies import (
    get_user,
    get_users,
    get_own_user,
    create_new_user,
    remove_user,
    remove_own_user,
)
from app.users.models import User, UserRead

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", response_model=UserRead)
async def create_user(user: Annotated[User, Depends(create_new_user)]):
    return user


@router.get("/id={user_id}", response_model=UserRead)
async def read_user(user: User = Depends(get_user)):
    return user


@router.get("/", response_model=list[UserRead])
async def read_users(
    users: Annotated[list[User], Depends(get_users)],
):
    return users


@router.get("/me", response_model=UserRead)
async def read_own_user(current_user: Annotated[User, Depends(get_own_user)]):
    return current_user


@router.delete("/id={user_id}", response_model=UserRead)
async def delete_user(user: User = Depends(remove_user)):
    return user


@router.delete("/me", response_model=UserRead)
async def delete_own_user(user: User = Depends(remove_own_user)):
    return user
