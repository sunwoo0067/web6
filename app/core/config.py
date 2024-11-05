<<<<<<< HEAD
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI"
    VERSION: str = "1.0.0"
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    DATABASE_URL: str = "mysql+pymysql://root:@localhost:3306/fastapi_test_db"

settings = Settings()
=======
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
>>>>>>> be5220edfd9c10ca47d60657c71d9ee5d1c8aeee
