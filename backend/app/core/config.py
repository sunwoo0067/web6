from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, field_validator

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Backend"
    
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode='before')
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database settings
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./sql_app.db"
    
    # JWT Settings
    SECRET_KEY: str = "your-secret-key-here"  # openssl rand -hex 32
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Zentrade API Settings
    ZENTRADE_API_URL: str = "https://www.zentrade.co.kr/shop/proc/order_api.php"
    ZENTRADE_API_ID: str = "b00679540"
    ZENTRADE_API_KEY: str = "5284c44b0fcf0f877e6791c5884d6ea9"

    model_config = SettingsConfigDict(case_sensitive=True)

settings = Settings()
