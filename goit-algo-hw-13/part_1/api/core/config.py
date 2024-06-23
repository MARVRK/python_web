
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    SECRET_KEY:str = "secret_key"
    SQLALCHEMY_DATABASE_URL:str = "postgresql+psycopg2://postgres:567234@localhost:5432/contact_db_1"
    SMTP_HOST:str = "smtp.gmail.com"
    SMTP_PORT:int = 587
    SMTP_USERNAME:str = "bfg578@gmail.com"
    SMTP_PASSWORD:str = "Wertixhp3490!@"  # Add your password here manually
    CLOUDINARY_CLOUD_NAME:str = "marv"
    CLOUDINARY_API_KEY:int = 792118963128647
    CLOUDINARY_API_SECRET: str = "Ab0nwzbLWpwDsfUGMtaJyRLZ7nY"
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    class Config:
        env_file = ".env"

settings = Settings()

