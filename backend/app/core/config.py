from pydantic_settings import BaseSettings
from pathlib import Path
import os

class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()