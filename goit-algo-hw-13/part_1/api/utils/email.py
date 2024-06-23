import os
from email.message import EmailMessage
import aiosmtplib
from jose import jwt
from datetime import datetime, timedelta
from api.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

def create_verification_token(email: str):
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
def create_reset_token(email: str):
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def send_verification_email(email: str, token: str):
    message = EmailMessage()
    message["From"] = settings.SMTP_USERNAME
    message["To"] = email
    message["Subject"] = "Email Verification"
    verification_link = f"http://your_domain/verify-email?token={token}"
    message.set_content(f"Please verify your email by clicking on the following link: {verification_link}")

    await aiosmtplib.send(
        message,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        start_tls=True,
        username=settings.SMTP_USERNAME,
        password=settings.SMTP_PASSWORD
    )
