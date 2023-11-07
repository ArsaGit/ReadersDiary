from typing import Annotated
import jwt

from fastapi import Depends, HTTPException, status

from app.utils.security import oauth2_scheme, decode_jwt
from app.schemas.api.user import UserCreate
from app.schemas.api.token import TokenData
from app.models.user_models import User
from app.services.user_service import UserService


async def authenticate_user(
    service: UserService,
    email: str,
    password: str,
):
    user = await service.get_by_email(email)
    if not user:
        return False
    if not user.check_password(password):
        return False
    return user


async def signup_new_user(
    service: UserService,
    email: str,
    password: str,
):
    user = await service.get_by_email(email)
    if user:
        return False
    return await service.create(
        UserCreate(email=email,
                   password=password,
                   is_active=True,
                   is_superuser=False,)
    )


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    service: UserService = Depends(),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_jwt(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.PyJWKError:
        raise credentials_exception
    user = await service.get_by_email(token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.is_active:
        return current_user
    else:
        raise HTTPException(status_code=400, detail="Inactive user")


async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user
