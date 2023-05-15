from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    env_name: str = "LOCAL"
    instance_host: str = "34.100.136.39"
    db_user: str = "shorty"
    db_pass: str = "j@!shreeR@m"
    db_name: str = "postgres"
    db_port: int = "5432"
    db_driver: str = "postgresql+asyncpg"

    # db_url: str = f"postgresql+asyncpg://{db_user}:{db_pass}@{instance_host}:{db_port}/{db_name}"

    # base_url: str = "http://localhost:8000"

    class Config:
        env_file = ".env"


@lru_cache(maxsize=10)
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.instance_host}")
    return settings
