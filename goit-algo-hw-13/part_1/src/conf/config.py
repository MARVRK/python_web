# config.py
from pydantic import EmailStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    SQLALCHEMY_DATABASE_URL: str
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: EmailStr
    SMTP_PASSWORD: str
    MAIL_FROM: EmailStr
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: int
    CLOUDINARY_API_SECRET: str
    REDIS_HOST: str
    REDIS_PORT: int
    ALGORITHM: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

config = Settings()
