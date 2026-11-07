from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    APP_NAME: str = "FileForge"
    DEBUG: bool = False
    
    # File limits (bytes)
    MAX_IMAGE_SIZE: int = 50 * 1024 * 1024      # 50 MB
    MAX_VIDEO_SIZE: int = 500 * 1024 * 1024     # 500 MB
    MAX_AUDIO_SIZE: int = 100 * 1024 * 1024     # 100 MB
    MAX_DOC_SIZE: int = 25 * 1024 * 1024        # 25 MB
    MAX_PDF_SIZE: int = 50 * 1024 * 1024        # 50 MB
    MAX_ARCHIVE_SIZE: int = 200 * 1024 * 1024   # 200 MB
    MAX_DEFAULT_SIZE: int = 20 * 1024 * 1024    # 20 MB
    
    # Rate limits
    ANON_FILES_PER_HOUR: int = 10
    USER_FILES_PER_HOUR: int = 100
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Job TTL (seconds)
    JOB_TTL: int = 3600  # 1 hour
    
    # JWT
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24h
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
