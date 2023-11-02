from typing import Annotated
import jwt

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user import get_user_by_email, create_user
from app.utils.security import verify_password, oauth2_scheme
from app.configs.environment import get_config
from app.configs.database import get_db_session
from app.schemas.api.user import UserCreate
from app.schemas.api.token import TokenData
from app.models.user_models import User

config = get_config()


async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def signup_new_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if user:
        return False
    new_user = await create_user(
        db,
        UserCreate(
            email=email,
            is_active=True,
            is_superuser=False,
            password=password,
        ),
    )
    return new_user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           db: AsyncSession = Depends(get_db_session),):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,
                             config.JWT_SECRET,
                             algorithms=[config.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.PyJWKError:
        raise credentials_exception
    user = await get_user_by_email(db, token_data.email)
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
