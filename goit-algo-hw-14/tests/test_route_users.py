import pickle
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from src.main import app
from src.entity.models import User
from src.schemas.user import UserResponse


client = TestClient(app)

# Fixtures to mock the dependencies
@pytest.fixture
def mock_db():
    return AsyncMock(spec=AsyncSession)

@pytest.fixture
def mock_current_user():
    return User(id=1, email="test@example.com")

@pytest.fixture
def mock_user_response():
    return UserResponse(id=1, email="test@example.com", username="John", is_active=True)

# Mock auth_service.get_current_user
@pytest.fixture(autouse=True)
def override_get_current_user():
    with patch("src.services.auth.auth_service.get_current_user") as mock:
        mock.return_value = User(id=1, email="test@example.com")
        yield mock

# Mock cloudinary
@pytest.fixture(autouse=True)
def mock_cloudinary():
    with patch("src.routes.users.cloudinary.uploader.upload") as mock_upload, \
         patch("src.routes.users.cloudinary.CloudinaryImage") as mock_image:
        mock_upload.return_value = {"version": "v1"}
        mock_image.return_value.build_url.return_value = "http://example.com/avatar.jpg"
        yield mock_upload, mock_image

# Test cases
def test_get_current_user(mock_current_user, mock_user_response):
    response = client.get("/users/me")
    assert response.status_code == 200
    assert response.json() == mock_user_response.dict()

def test_update_avatar(mock_db, mock_current_user, mock_user_response):
    file = {"file": ("avatar.jpg", b"fake image data", "image/jpeg")}
    with patch("src.repository.users.update_avatar_url", return_value=mock_user_response):
        response = client.patch("/users/avatar", files=file)
        assert response.status_code == 200
        assert response.json() == mock_user_response.dict()

def test_update_avatar_cloudinary(mock_db, mock_current_user):
    with patch("src.repository.users.update_avatar_url") as mock_update_avatar_url, \
         patch("src.services.auth.auth_service.cache.set") as mock_cache_set, \
         patch("src.services.auth.auth_service.cache.expire") as mock_cache_expire:
        mock_update_avatar_url.return_value = mock_current_user
        file = {"file": ("avatar.jpg", b"fake image data", "image/jpeg")}
        response = client.patch("/users/avatar", files=file)
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"
        mock_cache_set.assert_called_once_with("test@example.com", pickle.dumps(mock_current_user))
        mock_cache_expire.assert_called_once_with("test@example.com", 300)

def test_update_avatar_invalid_cloud_name():
    response = client.patch("/api/users/testing-avatar-upload")
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal Server Error"
