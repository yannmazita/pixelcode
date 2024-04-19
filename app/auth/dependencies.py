import os
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from pydantic import ValidationError

from app.dependencies import get_user_by_username
from app.auth.models import TokenData

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login",
    scopes={
        "user.create": "The ability to create a new user.",
        "user:own": "Read only access to the current user's information.",
        "user:own.write": "The ability to change the current user's information.",
        "user:own:player": "Read only access to the current user's player.",
        "user:own:player.write": "The ability to change the current user's player.",
        "user:others:player:points": "Read only access to players' points.",
        "user:others:player:playername": "Read only access to players' playernames.",
        "websockets": "Access to the websocket.",
        "admin": "Full access to all information.",
    },
    auto_error=True,
)


async def validate_token(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
) -> TokenData:
    """Validate token and check if it has the required scopes.
    Args:
        security_scopes: Scopes required by the dependent.
        token: Token to validate.
    Returns:
        A TokenData instance representing the token data.
    """
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    permissions_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not enough permissions",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception

    try:
        assert token_data.username is not None
        user = await get_user_by_username(token_data.username)
        user_scopes: list[str] = user.roles.split(" ")
        # Iterating through token scopes against scopes defined in user instance.
        for scope in token_data.scopes:
            if scope not in user_scopes:
                print(f"scope {scope} not in {user_scopes}")
                raise permissions_exception
    except HTTPException as e:
        raise e

    # Iterating through dependent's scopes against scopes defined in token.
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise permissions_exception
    return token_data
