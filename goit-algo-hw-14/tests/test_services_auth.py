import pytest
from unittest.mock import patch, AsyncMock
from datetime import datetime, timedelta
from src.services.auth import Auth
from src.entity.models import User
from src.conf.config import config
from jose import jwt

auth_service = Auth()

@pytest.fixture
def mock_user():
    hashed_password = auth_service.get_password_hash("password")
    return User(id=1, email="test@example.com", password=hashed_password,is_active=True)

@pytest.fixture(autouse=True)
def mock_jwt():
    with patch("src.services.auth.jwt.encode") as mock_encode, \
         patch("src.services.auth.jwt.decode") as mock_decode:
        mock_encode.return_value = "fake_token"
        mock_decode.return_value = {
            "sub": "test@example.com",
            "exp": (datetime.utcnow() + timedelta(minutes=15)).timestamp(),
            "scope": "access_token"
        }
        yield mock_encode, mock_decode

def test_verify_password(mock_user):
    assert auth_service.verify_password("password", mock_user.password)

def test_get_password_hash():
    password = "password"
    hashed_password = auth_service.get_password_hash(password)
    assert hashed_password != password
    assert auth_service.verify_password(password, hashed_password)

@pytest.mark.asyncio
async def test_create_access_token():
    data = {"sub": "test@example.com"}
    token = await auth_service.create_access_token(data)
    assert token == "fake_token"

@pytest.mark.asyncio
async def test_create_refresh_token():
    data = {"sub": "test@example.com"}
    token = await auth_service.create_refresh_token(data)
    assert token == "fake_token"

@pytest.mark.asyncio
async def test_decode_refresh_token():
    refresh_token = "fake_token"
    email = await auth_service.decode_refresh_token(refresh_token)
    assert email == "test@example.com"

@pytest.mark.asyncio
async def test_get_current_user(mock_db, mock_user):
    with patch("src.repository.users.get_user_by_email", return_value=mock_user):
        user = await auth_service.get_current_user("fake_token", mock_db)
        assert user.email == mock_user.email

def test_create_email_token():
    data = {"sub": "test@example.com"}
    token = auth_service.create_email_token(data)
    assert token == "fake_token"

@pytest.mark.asyncio
async def test_get_email_from_token():
    token = "fake_token"
    email = await auth_service.get_email_from_token(token)
    assert email == "test@example.com"
