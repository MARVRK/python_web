import pytest
from unittest.mock import AsyncMock
from src.entity.models import User
from src.schemas.user import UserCreate
from src.repository.users import (
    create_user,
    get_user_by_email,
    update_token,
    confirmed_email,
    update_avatar_url
)

@pytest.fixture
def mock_db():
    return AsyncMock()

@pytest.fixture
def mock_user():
    return User(
        id=1,
        username="John Doe",
        password="password",
        avatar="http://",
        confirmed=True,
        is_active=True,
        email="john.doe@example.com"
    )

@pytest.fixture
def mock_user_create():
    return UserCreate(
        email="john.doe@example.com",
        username="John Doe",
        password="password"
    )

@pytest.mark.asyncio
async def test_get_user_by_email(mock_db, mock_user):
    mock_db.execute.return_value.scalar_one_or_none.return_value = mock_user
    user = await get_user_by_email("john.doe@example.com", mock_db)
    assert user == mock_user

@pytest.mark.asyncio
async def test_create_user(mock_db, mock_user_create):
    mock_db.refresh = AsyncMock()
    new_user = await create_user(mock_user_create, mock_db)
    assert new_user.email == mock_user_create.email
    assert new_user.username == mock_user_create.username

@pytest.mark.asyncio
async def test_update_token(mock_db, mock_user):
    mock_user.refresh_token = None
    await update_token(mock_user, "new_token", mock_db)
    assert mock_user.refresh_token == "new_token"

@pytest.mark.asyncio
async def test_confirmed_email(mock_db, mock_user):
    mock_db.execute.return_value.scalar_one_or_none.return_value = mock_user
    await confirmed_email("john.doe@example.com", mock_db)
    assert mock_user.confirmed == True

@pytest.mark.asyncio
async def test_update_avatar_url(mock_db, mock_user):
    mock_db.execute.return_value.scalar_one_or_none.return_value = mock_user
    new_avatar_url = "http://new-avatar-url.com"
    updated_user = await update_avatar_url("john.doe@example.com", new_avatar_url, mock_db)
    assert updated_user.avatar == new_avatar_url

