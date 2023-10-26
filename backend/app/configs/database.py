from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)

from app.configs.environment import get_environment_variables


env = get_environment_variables()

Engine = create_async_engine(env.POSTGRES_URL.unicode_string(),
                             echo=env.DEBUG_MODE,
                             future=True)

AsyncSessionFactory = async_sessionmaker(Engine,
                                         autoflush=False,
                                         expire_on_commit=False,)


async def get_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        yield session
