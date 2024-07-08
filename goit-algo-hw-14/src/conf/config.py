
from pydantic import EmailStr
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    """
    A class to hold application settings.

    Attributes:
    SECRET_KEY: str : Secret key for the application.
    SQLALCHEMY_DATABASE_URL: str : Database connection URL.
    SMTP_HOST: str : SMTP server host.
    SMTP_PORT: int : SMTP server port.
    SMTP_USERNAME: EmailStr : SMTP server username.
    SMTP_PASSWORD: str : SMTP server password.
    MAIL_FROM: EmailStr : Default email address for sending emails.
    CLOUDINARY_CLOUD_NAME: str : Cloudinary cloud name.
    CLOUDINARY_API_KEY: int : Cloudinary API key.
    CLOUDINARY_API_SECRET: str : Cloudinary API secret.
    REDIS_HOST: str : Redis server host.
    REDIS_PORT: int : Redis server port.
    ALGORITHM: str : Algorithm for JWT.

    Methods:
    None
    """

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
        """
        Configuration settings for the Settings class.

        Attributes:
        env_file: str : Path to the .env file.
        env_file_encoding: str : Encoding of the .env file.

        Methods:
        None
        """

        env_file = ".env"
        env_file_encoding = "utf-8"

# Instantiate the Settings class and load environment variables from.env file.
config = Settings(_env_file=os.path.abspath(os.path.join(os.path.dirname(__file__), '../../.env')))
