from fastapi import (
    Depends,
    status,
    APIRouter,
    Request
)
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.environment import get_config
from app.configs.database import get_db_session
from app.schemas.api.user import UserSchema, UserCreate
from app.repositories import user as user_repo
from app.services.auth import get_current_active_user

config = get_config()
users_router = r = APIRouter()


@r.post("/users",
        response_model=UserSchema,
        status_code=status.HTTP_201_CREATED,
        response_model_exclude_none=True)
async def create_user(request: Request,
                      payload: UserCreate,
                      db: AsyncSession = Depends(get_db_session)):
    user = await user_repo.create_user(db, payload)
    return user


@r.get("/users/me",
       response_model=UserSchema,
       status_code=status.HTTP_200_OK,
       response_model_exclude_none=True,)
async def get_users_me(
    request: Request,
    current_user: UserSchema = Depends(get_current_active_user),
):
    return current_user


@r.get("/users/{user_id}",
       response_model=UserSchema,
       status_code=status.HTTP_200_OK,
       response_model_exclude_none=True)
async def get_user(request: Request,
                   user_id: int,
                   db: AsyncSession = Depends(get_db_session)):
    user = await user_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    return user


@r.get("/users",
       response_model=list[UserSchema],
       status_code=status.HTTP_200_OK,
       response_model_exclude_none=True)
async def get_users_list(request: Request,
                         db: AsyncSession = Depends(get_db_session)):
    users = await user_repo.get_users(db)
    return users
