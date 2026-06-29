from functools import lru_cache
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


# ==========================
# Application Settings
# ==========================

class AppSettings(BaseModel):
    name: str = "ResearchOS"
    version: str = "0.1.0"
    environment: Literal["development", "testing", "production"] = "development"


# ==========================
# API Settings
# ==========================

class ApiSettings(BaseModel):
    prefix: str = "/api"
    version_prefix: str = "/v1"
    host: str = "0.0.0.0"
    port: int = 8000


# ==========================
# Logging Settings
# ==========================

class LoggingSettings(BaseModel):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"


# ==========================
# Database Settings
# ==========================

class DatabaseSettings(BaseModel):
    url: str = "sqlite+aiosqlite:///./researchos.db"


# ==========================
# JWT Settings
# ==========================

class JWTSettings(BaseModel):
    secret_key: str = "CHANGE_ME_IN_PRODUCTION"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60


# ==========================
# Main Settings
# ==========================

class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    api: ApiSettings = ApiSettings()
    logging: LoggingSettings = LoggingSettings()
    database: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings()

    model_config = SettingsConfigDict(
    env_file=".env",
    env_nested_delimiter="__",
    case_sensitive=False,
    extra="ignore",
)


@lru_cache
def get_settings() -> Settings:
    return Settings()