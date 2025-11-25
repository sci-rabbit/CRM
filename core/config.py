from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = Field(
        default="sqlite+aiosqlite:///./crm.db",
        alias="DATABASE_URL",
    )


settings = Settings()
