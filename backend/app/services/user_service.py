from fastapi import Depends
from typing import List

from app.repositories.user_repository import UserRepository
from app.models.user_models import User
from app.schemas.api.user import UserCreate


class UserService:
    user_repo: UserRepository

    def __init__(self, user_repo: UserRepository = Depends()) -> None:
        self.user_repo = user_repo

    async def create(self, user_body: UserCreate) -> User:
        user_dict = user_body.model_dump()
        return await self.user_repo.create(User(**user_dict))

    async def get(self, user_id: int) -> User:
        return await self.user_repo.get(user_id)

    async def get_list(self) -> List[User]:
        return await self.user_repo.get_list()

    async def delete(self, user_id: int) -> None:
        return await self.user_repo.delete(User(id=user_id))

    async def get_by_email(self, email: str) -> User | None:
        return await self.user_repo.get_by_email(email)
