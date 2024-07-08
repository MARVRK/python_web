from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from src.main import app
from src.schemas.contacts import ContactCreate, ContactResponse, UpcomingBirthdaysResponse
from src.entity.models import User

client = TestClient(app)

@pytest.fixture
def mock_db():
    return AsyncMock(spec=AsyncSession)

@pytest.fixture
def mock_current_user():
    return User(id=1, email="test@example.com")

@pytest.fixture
def mock_contact():
    return ContactResponse(id=1, name="John", email="john@example.com", surename ="Doe", phone_number="11213131",birthday=datetime (1990,1,1))

# Mock auth_service.get_current_user
@pytest.fixture(autouse=True)
def override_get_current_user():
    with patch("src.services.auth.auth_service.get_current_user") as mock:
        mock.return_value = User(id=1, email="test@example.com")
        yield mock

# Test cases
def test_create_contact(mock_db, mock_current_user, mock_contact):
    contact_data = {"name": "John Doe", "email": "john@example.com"}
    with patch("src.repository.contacts.create_contact", return_value=mock_contact):
        response = client.post("/contacts", json=contact_data)
        assert response.status_code == 201
        assert response.json() == mock_contact.dict()

def test_read_contact(mock_db, mock_current_user, mock_contact):
    contact_id = 1
    with patch("src.repository.contacts.get_contact_by_id", return_value=mock_contact):
        response = client.get(f"/contact/{contact_id}")
        assert response.status_code == 200
        assert response.json() == mock_contact.dict()

def test_read_contacts(mock_db, mock_current_user, mock_contact):
    with patch("src.repository.contacts.get_contacts", return_value=[mock_contact]):
        response = client.get("/contacts")
        assert response.status_code == 200
        assert response.json() == [mock_contact.dict()]

def test_update_contact(mock_db, mock_current_user, mock_contact):
    contact_id = 1
    contact_data = {"name": "John Doe", "email": "john@example.com"}
    with patch("src.repository.contacts.update_contact", return_value=mock_contact):
        response = client.put(f"/contacts/{contact_id}", json=contact_data)
        assert response.status_code == 200
        assert response.json() == mock_contact.dict()

def test_delete_contact(mock_db, mock_current_user):
    contact_id = 1
    with patch("src.repository.contacts.delete_contact", return_value=None):
        response = client.delete(f"/contacts/{contact_id}")
        assert response.status_code == 204

def test_upcoming_birthdays(mock_db, mock_current_user):
    upcoming_birthdays = [{"name": "John Doe", "surename": "Doe", "date_of_birth": "2000-01-01"}]
    with patch("src.repository.contacts.get_upcoming_birthdays", return_value=upcoming_birthdays):
        response = client.get("/contacts/upcoming_birthdays")
        assert response.status_code == 200
        assert response.json() == upcoming_birthdays
