from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import MongoDsn, PostgresDsn, RedisDsn


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "TashRent API"
    debug: bool = False

    postgres_url: PostgresDsn
    mongo_url: MongoDsn
    redis_url: RedisDsn


@lru_cache
def get_settings() -> Settings:
    return Settings()