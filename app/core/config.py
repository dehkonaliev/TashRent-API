from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "TashRent API"
    debug: bool = False

    postgres_url: str
    mongo_url: str
    redis_url: str


@lru_cache
def get_settings() -> Settings:
    return Settings()