from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str = os.environ.get("DB_URL", "sqlite://store.db")
    PORT: int = os.environ.get("PORT", 8000)
