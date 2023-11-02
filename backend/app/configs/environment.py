from functools import lru_cache
import os

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"


class EnvironmentSettings(BaseSettings):
    APP_NAME: str

    DEBUG_MODE: bool

    HOST_URL: str
    HOST_PORT: int

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_ASYNC_URL: PostgresDsn
    POSTGRES_URL: PostgresDsn

    JWT_EXPIRE_MINUTES: int
    JWT_ALGORITHM: str
    JWT_SECRET: str

    model_config = SettingsConfigDict(
        env_file=get_env_filename(),
        env_file_encoding="utf-8"
    )


@lru_cache
def get_config():
    return EnvironmentSettings()
