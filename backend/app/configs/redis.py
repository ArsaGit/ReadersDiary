import redis.asyncio as redis

from app.configs.environment import get_environment_variables


env = get_environment_variables()


async def get_redis():
    return await redis.from_url(
        env.REDIS_URL.unicode_string(),
        encoding="utf-8",
        decode_responses=True,
    )
