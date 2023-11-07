from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import List

from app.configs.database import get_db_session, get_init_db
from app.models.user_models import User


class UserRepository:
    def __init__(self,
                 async_session: AsyncSession = Depends(get_db_session),
                 sync_session: Session = Depends(get_init_db)):
        self.async_db = async_session
        self.sync_db = sync_session

    async def create(self, user: User) -> User:
        self.async_db.add(user)
        await self.async_db.commit()
        await self.async_db.refresh(user)
        return user

    async def get(self, id: int) -> User:
        return await self.async_db.get(User, id)

    async def get_list(self) -> List[User]:
        result = await self.async_db.scalars(select(User))
        return result.all()

    async def update(self, id: int, user: User) -> User:
        user.id = id
        self.async_db.merge(user)
        await self.async_db.commit()
        return user

    async def delete(self, user: User) -> None:
        self.async_db.delete(user)
        await self.async_db.commit()
        await self.async_db.flush()

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).filter_by(email=email)
        return await self.async_db.scalar(stmt)
