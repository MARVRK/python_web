import pytest
import os
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from src.main import app

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

@pytest.fixture(scope="module")
def client():
    with patch("src.main.redis.Redis") as mock_redis, \
            patch("src.main.FastAPILimiter.init") as mock_limiter:
        mock_redis.return_value.ping = AsyncMock(return_value=True)
        mock_limiter.return_value = AsyncMock()
        with TestClient(app) as c:
            yield c

@pytest.fixture
def mock_db():
    return AsyncMock()
