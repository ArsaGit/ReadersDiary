from typing import List
from fastapi import (
    Depends,
    status,
    APIRouter,
    Request
)
from fastapi.exceptions import HTTPException

from app.configs.environment import get_config
from app.schemas.api.user import UserSchema, UserCreate
from app.services.auth_service import (
    get_current_active_user,
    get_current_active_superuser,
)
from app.services.user_service import UserService

config = get_config()
users_router = r = APIRouter()


@r.post("/users",
        response_model=UserSchema,
        status_code=status.HTTP_201_CREATED,
        response_model_exclude_none=True)
async def create_user(
    request: Request,
    payload: UserCreate,
    service: UserService = Depends(),
    current_user=Depends(get_current_active_superuser)
):
    user = await service.create(payload)
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
async def get_user(
    request: Request,
    user_id: int,
    service: UserService = Depends(),
    current_user=Depends(get_current_active_superuser),
):
    user = await service.get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    return user


@r.get("/users",
       response_model=List[UserSchema],
       status_code=status.HTTP_200_OK,
       response_model_exclude_none=True)
async def get_users_list(
    request: Request,
    service: UserService = Depends(),
    current_user=Depends(get_current_active_superuser),
):
    users = await service.get_list()
    return users
