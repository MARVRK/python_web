# email.py

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr
from src.services.auth import auth_service
from src.conf.config import config
from pathlib import Path

conf = ConnectionConfig(
    MAIL_USERNAME=config.SMTP_USERNAME,
    MAIL_PASSWORD=config.SMTP_PASSWORD,
    MAIL_FROM=config.MAIL_FROM,
    MAIL_PORT=config.SMTP_PORT,
    MAIL_SERVER=config.SMTP_HOST,
    MAIL_FROM_NAME="Book of Contacts",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',)
"""
This function sends a verification email to the user's email address.

Parameters:
- email (EmailStr): The email address of the user.
- username (str): The username of the user.
- host (str): The host URL where the email verification link will be used.

Returns:
- None

Raises:
- ConnectionErrors: If there are any issues with the email connection.

"""
async def send_email(email: EmailStr, username: str, host: str):
    try:
        # Create a verification token for the email
        token_verification = auth_service.create_email_token({"sub": email})

        # Prepare the email message
        message = MessageSchema(
            subject="Confirm your email",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )

        # Initialize FastMail with the connection configuration
        fm = FastMail(conf)

        # Send the email using the prepared message and the email template
        await fm.send_message(message, template_name="verify_email.html")
    except ConnectionErrors as err:
        # Print any connection errors
        print(err)


async def send_email(email: EmailStr, username: str, host: str):
    """
    This function sends a verification email to the user's email address.

    Parameters:
    - email (EmailStr): The email address of the user.
    - username (str): The username of the user.
    - host (str): The host URL where the email verification link will be used.

    Returns:
    - None

    Raises:
    - ConnectionErrors: If there are any issues with the email connection.

    """
    try:
        # Create a verification token for the email
        token_verification = auth_service.create_email_token({"sub": email})

        # Prepare the email message
        message = MessageSchema(
            subject="Confirm your email",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )

        # Initialize FastMail with the connection configuration
        fm = FastMail(conf)

        # Send the email using the prepared message and the email template
        await fm.send_message(message, template_name="verify_email.html")
    except ConnectionErrors as err:
        # Print any connection errors
        print(err)
