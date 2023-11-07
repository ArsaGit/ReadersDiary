from typing import Annotated
from datetime import timedelta

from fastapi import (
    Depends,
    status,
    APIRouter
)
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException

from app.configs.environment import get_config
from app.schemas.api.token import Token
from app.utils.security import create_access_token
from app.services.auth_service import authenticate_user, signup_new_user
from app.services.user_service import UserService

config = get_config()
auth_router = r = APIRouter()


@r.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(),
):
    user = await authenticate_user(user_service,
                                   form_data.username,
                                   form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # create token
    access_token_expires = timedelta(minutes=config.JWT_EXPIRE_MINUTES)
    if user.is_superuser:
        permissions = "admin"
    else:
        permissions = "user"
    access_token = create_access_token(
        data={"sub": user.email, "permissions": permissions},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@r.post("/signup", response_model=Token)
async def signup(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(),
):
    user = await signup_new_user(user_service,
                                 form_data.username,
                                 form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # create token
    access_token_expires = timedelta(minutes=config.JWT_EXPIRE_MINUTES)
    if user.is_superuser:
        permissions = "admin"
    else:
        permissions = "user"
    access_token = create_access_token(
        data={"sub": user.email, "permissions": permissions},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
