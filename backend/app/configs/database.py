
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)

from app.configs.environment import get_environment_variables


env = get_environment_variables()
DATABASE_URL = f"{env.DATABASE_DIALECT}:{env.DATABASE_URI}"

Engine = create_async_engine(DATABASE_URL,
                             echo=env.DEBUG_MODE,
                             future=True)

AsyncSessionFactory = async_sessionmaker(Engine,
                                         autoflush=False,
                                         expire_on_commit=False,)


async def get_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        yield session
