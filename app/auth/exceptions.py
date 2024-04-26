from fastapi import HTTPException, status

incorrect_password = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect password",
    headers={"WWW-Authenticate": "Bearer"},
)

incorrect_username_or_password = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

username_already_exists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Username already exists",
    headers={"WWW-Authenticate": "Bearer"},
)
