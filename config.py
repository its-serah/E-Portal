"""
Configuration for FastAPI face recognition application.
"""

from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Project settings
    PROJECT_NAME: str = "Face Recognition System"
    DEBUG: bool = False
    SECRET_KEY: str = "your-secret-key-here"
    
    # Database
    USE_POSTGRESQL: bool = False
    DATABASE_URL: Optional[str] = None
    DB_NAME: str = "face_recognition"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    
    # Media paths
    BASE_DIR: Path = Path(__file__).parent
    MEDIA_ROOT: Path = BASE_DIR / "media"
    MEDIA_URL: str = "/media/"
    
    # JWT settings
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Email configuration
    EMAIL_BACKEND: Optional[str] = None
    EMAIL_HOST: Optional[str] = None
    EMAIL_PORT: int = 587
    EMAIL_USE_TLS: bool = True
    EMAIL_HOST_USER: Optional[str] = None
    EMAIL_HOST_PASSWORD: Optional[str] = None
    PASSWORD_RESET_TIMEOUT: int = 3600
    
    # Telegram configuration
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHANNEL_ID: Optional[str] = None
    
    def get_database_url(self) -> str:
        """Get the database URL based on configuration."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        
        if self.USE_POSTGRESQL:
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        else:
            db_path = self.BASE_DIR / "face_recognition.db"
            return f"sqlite:///{db_path}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
