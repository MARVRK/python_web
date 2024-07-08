import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock

from src.main import app

@pytest.mark.asyncio
@patch('src.repository.users.get_user_by_email')
@patch('src.services.auth.auth_service.get_password_hash')
@patch('src.repository.users.create_user')
@patch('src.services.email.send_email')
async def test_signup(mock_send_email, mock_create_user, mock_get_password_hash, mock_get_user_by_email, client):
    mock_get_user_by_email.return_value = None
    mock_get_password_hash.return_value = "hashed_password"
    mock_create_user.return_value = AsyncMock(email="test.user@example.com", username="testuser")

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/auth/signup", json={
            "email": "test.user@example.com",
            "username": "testuser",
            "password": "testpassword"
        })

    assert response.status_code == 201
    assert response.json()["email"] == "test.user@example.com"
    assert response.json()["username"] == "testuser"

@pytest.mark.asyncio
@patch('src.repository.users.get_user_by_email')
@patch('src.services.auth.auth_service.verify_password')
@patch('src.services.auth.auth_service.create_access_token')
@patch('src.services.auth.auth_service.create_refresh_token')
@patch('src.repository.users.update_token')
async def test_login(mock_update_token, mock_create_refresh_token, mock_create_access_token, mock_verify_password, mock_get_user_by_email, client):
    mock_get_user_by_email.return_value = AsyncMock(email="test.user@example.com", password="hashed_password", confirmed=True)
    mock_verify_password.return_value = True
    mock_create_access_token.return_value = "access_token"
    mock_create_refresh_token.return_value = "refresh_token"

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/auth/login", data={
            "username": "test.user@example.com",
            "password": "testpassword"
        })

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

@pytest.mark.asyncio
@patch('src.repository.users.get_user_by_email')
@patch('src.services.auth.auth_service.decode_refresh_token')
@patch('src.services.auth.auth_service.create_access_token')
@patch('src.services.auth.auth_service.create_refresh_token')
@patch('src.repository.users.update_token')
async def test_refresh_token(mock_update_token, mock_create_refresh_token, mock_create_access_token, mock_decode_refresh_token, mock_get_user_by_email, client):
    mock_decode_refresh_token.return_value = "test.user@example.com"
    mock_get_user_by_email.return_value = AsyncMock(email="test.user@example.com", refresh_token="valid_refresh_token")
    mock_create_access_token.return_value = "new_access_token"
    mock_create_refresh_token.return_value = "new_refresh_token"

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/auth/refresh_token", headers={
            "Authorization": "Bearer valid_refresh_token"
        })

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

@pytest.mark.asyncio
@patch('src.repository.users.get_user_by_email')
@patch('src.services.auth.auth_service.get_email_from_token')
@patch('src.repository.users.confirmed_email')
async def test_confirmed_email(mock_confirmed_email, mock_get_email_from_token, mock_get_user_by_email, client):
    mock_get_email_from_token.return_value = "test.user@example.com"
    mock_get_user_by_email.return_value = AsyncMock(email="test.user@example.com", confirmed=False)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/auth/confirmed_email/test_token")

    assert response.status_code == 200
    assert response.json()["message"] == "Email confirmed"

@pytest.mark.asyncio
@patch('src.repository.users.get_user_by_email')
@patch('src.services.email.send_email')
async def test_request_email(mock_send_email, mock_get_user_by_email, client):
    mock_get_user_by_email.return_value = AsyncMock(email="test.user@example.com", confirmed=False)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/auth/request_email", json={
            "email": "test.user@example.com"
        })

    assert response.status_code == 200
    assert response.json()["message"] == "Check your email for confirmation."
