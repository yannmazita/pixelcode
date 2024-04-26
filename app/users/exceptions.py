from fastapi import HTTPException, status


user_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found.",
)

multiple_users_found = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Multiple users found with the same attribute.",
)

user_already_exists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User with this username already exists",
)
