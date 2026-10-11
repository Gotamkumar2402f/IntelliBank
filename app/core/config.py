from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "IntelliBank"
    DATABASE_URL: str = "sqlite:///./data/intellibank.db"
    SECRET_KEY: str = "supersecretkey123456789"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
   import os
   GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # ✅ From .env
    class Config:
        env_file = ".env"

settings = Settings()