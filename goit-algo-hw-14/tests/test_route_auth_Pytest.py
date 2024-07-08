import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_signup():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/signup", json={
            "email": "test.user@example.com",
            "username": "testuser",
            "password": "testpassword"
        })
    assert response.status_code == 201
    assert response.json()["email"] == "test.user@example.com"
    assert response.json()["username"] == "testuser"

@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/login", data={
            "username": "test.user@example.com",
            "password": "testpassword"
        })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

@pytest.mark.asyncio
async def test_refresh_token():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        login_response = await ac.post("/auth/login", data={
            "username": "test.user@example.com",
            "password": "testpassword"
        })
        refresh_token = login_response.json()["refresh_token"]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/auth/refresh_token", headers={
            "Authorization": f"Bearer {refresh_token}"
        })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

@pytest.mark.asyncio
async def test_confirmed_email():
    token = "generated_token_for_confirmation"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/auth/confirmed_email/{token}")
    assert response.status_code == 200
    assert response.json()["message"] == "Email confirmed"

@pytest.mark.asyncio
async def test_request_email():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/request_email", json={
            "email": "test.user@example.com"
        })
    assert response.status_code == 200
    assert response.json()["message"] == "Check your email for confirmation."
