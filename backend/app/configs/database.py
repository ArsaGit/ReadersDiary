from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.configs.environment import get_config


env = get_config()
ASYNC_DATABASE_URL = env.POSTGRES_ASYNC_URL.unicode_string()
DATABASE_URL = env.POSTGRES_URL.unicode_string()

engine = create_async_engine(ASYNC_DATABASE_URL,
                             echo=env.DEBUG_MODE,
                             future=True)
init_engine = create_engine(DATABASE_URL,
                            future=True)

async_session_factory = async_sessionmaker(engine,
                                           autoflush=False,
                                           expire_on_commit=False,)
session_factory = sessionmaker(init_engine,
                               autoflush=True,
                               expire_on_commit=False,)


async def get_db_session() -> AsyncGenerator:
    async with async_session_factory() as session:
        yield session


def get_init_db():
    return session_factory()
