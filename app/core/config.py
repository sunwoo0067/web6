from pydantic import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Example"
    VERSION: str = "1.0.0"
    
    class Config:
        case_sensitive = True

settings = Settings() 