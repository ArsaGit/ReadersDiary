from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.utils import security
from app.models.user_models import User
from app.schemas.api.user import UserCreate


async def create_user(db: AsyncSession,
                      user: UserCreate):
    hashed_pass = security.get_password_hash(user.password)
    db_user = User(email=user.email,
                   username=user.username,
                   is_active=user.is_active,
                   is_superuser=user.is_superuser,
                   hashed_password=hashed_pass)
    db.add(db_user)
    await db.commit()
    return db_user


async def get_user(db: AsyncSession, id: int):
    user = await db.get(User, id)
    return user


async def get_users(db: AsyncSession):
    users = await db.scalars(select(User))
    return users.all()


async def get_user_by_email(db: AsyncSession, email: str):
    user = await db.scalar(select(User).where(User.email == email))
    return user


def create_user_sync(db: Session,
                     user: UserCreate):
    hashed_pass = security.get_password_hash(user.password)
    db_user = User(email=user.email,
                   username=user.username,
                   is_active=user.is_active,
                   is_superuser=user.is_superuser,
                   hashed_password=hashed_pass)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
