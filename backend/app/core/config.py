﻿from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRATION_TIME: int
    REFRESH_TOKEN_EXPIRATION_TIME: int
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    JWT_ALGORITHM: str
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str
    FRONTEND_DOMAIN: str
    RESET_PASSWORD_TOKEN_EXPIRY_MINUTES: int
    EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS: int

    class Config:
        env_file = ".env"

settings = Settings()