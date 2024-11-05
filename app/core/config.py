<<<<<<< HEAD
from pydantic_settings import BaseSettings
=======
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
>>>>>>> b2ce390b7110b42e0cbce41d29456a94019515dc
from typing import Optional

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Example"
    VERSION: str = "1.0.0"
    
    # XAMPP MySQL 
    DATABASE_URL: str = "mysql+pymysql://root:@localhost:3306/fastapi_db"
    
    # JWT 
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Zentrade API Settings
    ZENTRADE_API_URL: str = "https://www.zentrade.co.kr/shop/proc/order_api.php"
    ZENTRADE_API_ID: str = "b00679540"
    ZENTRADE_API_KEY: str = "5284c44b0fcf0f877e6791c5884d6ea9"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
<<<<<<< HEAD
=======
>>>>>>> be5220edfd9c10ca47d60657c71d9ee5d1c8aeee
>>>>>>> b2ce390b7110b42e0cbce41d29456a94019515dc
