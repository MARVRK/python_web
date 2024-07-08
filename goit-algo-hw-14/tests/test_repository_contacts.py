import pytest
from unittest.mock import AsyncMock
from datetime import datetime,timedelta
from src.entity.models import Contact
from src.schemas.contacts import ContactCreate
from src.repository.contacts import (get_contacts,
	get_contact_by_id,
	create_contact,
	update_contact,
	delete_contact,
	get_upcoming_birthdays)

@pytest.fixture
def mock_db ():
	return AsyncMock ()

@pytest.fixture
def mock_contact ():
	return Contact (id=1,
					owner_id=1,
					name="John Doe",
					email="john.doe@example.com",
					birthday=datetime (1990,1,1))

@pytest.fixture
def mock_contact_create ():
	return ContactCreate (name="John",
						  surename= "Doe",
					      phone_number= "18181818",
						  email="john.doe@example.com",
						  birthday=datetime (1990,1,1))

@pytest.mark.asyncio
async def test_get_contacts (mock_db,
		mock_contact):
	mock_db.execute.return_value.scalars.return_value.all.return_value = [mock_contact]

	contacts = await get_contacts (mock_db,
		owner_id=1)
	assert contacts == [mock_contact]

@pytest.mark.asyncio
async def test_get_contact_by_id (mock_db,
		mock_contact):
	mock_db.execute.return_value.scalars.return_value.first.return_value = mock_contact

	contact = await get_contact_by_id (mock_db,
		contact_id=1,
		owner_id=1)
	assert contact == mock_contact

@pytest.mark.asyncio
async def test_create_contact (mock_db,
		mock_contact_create):
	mock_db.refresh = AsyncMock ()
	new_contact = await create_contact (mock_db,
		contact=mock_contact_create,
		user_id=1)

	assert new_contact.owner_id == 1
	assert new_contact.name == mock_contact_create.name

@pytest.mark.asyncio
async def test_update_contact (mock_db,
		mock_contact,
		mock_contact_create):
	mock_db.execute.return_value.scalars.return_value.first.return_value = mock_contact
	mock_db.commit = AsyncMock ()
	mock_db.refresh = AsyncMock ()

	updated_contact = await update_contact (mock_db,
		contact_id=1,
		contact_data=mock_contact_create,
		owner_id=1)
	assert updated_contact.name == mock_contact_create.name

@pytest.mark.asyncio
async def test_delete_contact (mock_db,
		mock_contact):
	mock_db.execute.return_value.scalars.return_value.first.return_value = mock_contact
	mock_db.commit = AsyncMock ()

	deleted_contact = await delete_contact (mock_db,
		contact_id=1,
		owner_id=1)
	assert deleted_contact == mock_contact

@pytest.mark.asyncio
async def test_get_upcoming_birthdays (mock_db,
		mock_contact):
	mock_db.execute.return_value.scalars.return_value.all.return_value = [mock_contact]

	upcoming_birthdays = await get_upcoming_birthdays (mock_db,
		owner_id=1)
	assert mock_contact in upcoming_birthdays
