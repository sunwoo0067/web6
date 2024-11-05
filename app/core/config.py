from typing import Optional
from pydantic import BaseSettings, MySQLDsn

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Example"
    VERSION: str = "1.0.0"
    
    # JWT settings
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # Database settings
    DATABASE_URL: Optional[MySQLDsn] = None

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()