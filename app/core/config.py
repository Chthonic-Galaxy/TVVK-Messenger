from pydantic import (
    PostgresDsn
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_ignore_empty=True, extra="ignore",
        case_sensitive=True
    )
    
    # Backend
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Messenger"
    BACKEND_CORS_ORIGINS: list[str] = ["*"] # Allow all sources (for development)
    
    # DataBase
    DB_ECHO: bool = False
    
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    
    # Auth
    AUTH_SECRET_KEY: str
    AUTH_ALGORITHM: str = "HS256"
    AUTH_DEFAULT_ACCESS_TOKEN_EXP_MIN: int = 30
    
    def database_url(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME,
        )

settings = Settings()
