from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str


def get_settings() -> Settings:
    return Settings(
        DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:5432/postgres",
        #DATABASE_URL = "postgresql+asyncpg://postgres:admin@127.0.0.1:5432/postgres",
    )