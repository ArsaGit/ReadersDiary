from functools import lru_cache
import os

from pydantic import RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"


class EnvironmentSettings(BaseSettings):
    APP_NAME: str
    DATABASE_DIALECT: str
    DATABASE_URI: str
    DEBUG_MODE: bool
    HOST_URL: str
    HOST_PORT: int
    JWT_EXPIRE: int
    JWT_ALGORITHM: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_URL: RedisDsn

    model_config = SettingsConfigDict(
        env_file=get_env_filename(),
        env_file_encoding="utf-8"
    )


@lru_cache
def get_environment_variables():
    return EnvironmentSettings()
