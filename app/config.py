from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Pydantic validates types automatically.
    """
    # Database
    DATABASE_URL: str
    
    # JWT Settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Redis
    REDIS_URL: str
    
    # App Info
    APP_NAME: str = "Buzzprime API"
    VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"  # Loads from .env file
        case_sensitive = True

@lru_cache()  # Cache settings so we don't reload every time
def get_settings() -> Settings:
    return Settings()

settings = get_settings()