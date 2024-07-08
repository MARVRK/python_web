from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.entity.models import Contact
from src.schemas.contacts import ContactCreate
from typing import Optional, List
from datetime import datetime, timedelta

async def get_contacts(db: AsyncSession,
        owner_id: int,
        skip: int = 0,
        limit: int = 10,
        name: Optional[str] = None,
        surname: Optional[str] = None,
        email: Optional[str] = None) -> List[Contact]:
    """
    Fetch a list of contacts based on the provided filters and pagination parameters.

    Parameters:
    db (AsyncSession): The database session for asynchronous operations.
    owner_id (int): The ID of the owner of the contacts.
    skip (int, optional): The number of contacts to skip for pagination. Default is 0.
    limit (int, optional): The maximum number of contacts to return. Default is 10.
    name (str, optional): The name filter for contacts. Default is None.
    surname (str, optional): The surname filter for contacts. Default is None.
    email (str, optional): The email filter for contacts. Default is None.

    Returns:
    List[Contact]: A list of contacts that match the provided filters and pagination parameters.
    """
    query = select(Contact).where(Contact.owner_id == owner_id)

    if name:
        query = query.where(Contact.name.ilike(f"%{name}%"))
    if surname:
        query = query.where(Contact.surname.ilike(f"%{surname}%"))
    if email:
        query = query.where(Contact.email.ilike(f"%{email}%"))

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    contacts = result.scalars().all()
    return contacts

async def get_contact_by_id(db: AsyncSession, contact_id: int, owner_id: int) -> Optional[Contact]:
    """
    Fetch a contact by its ID and owner ID.

    Parameters:
    db (AsyncSession): The database session for asynchronous operations.
    contact_id (int): The ID of the contact to fetch.
    owner_id (int): The ID of the owner of the contact.

    Returns:
    Optional[Contact]: The contact with the specified ID and owner ID, or None if not found.
    """
    query = select(Contact).where(Contact.id == contact_id, Contact.owner_id == owner_id)
    result = await db.execute(query)
    return result.scalars().first()

async def create_contact(db: AsyncSession, contact: ContactCreate, user_id: int) -> Contact:
    """
    Create a new contact in the database.

    Parameters:
    db (AsyncSession): The database session for asynchronous operations.
    contact (ContactCreate): The contact data to be created.
    user_id (int): The ID of the user who is creating the contact.

    Returns:
    Contact: The newly created contact.

    Raises:
    Exception: If any error occurs during the database operation.
    """
    new_contact = Contact(**contact.dict(), owner_id=user_id)  # Create a new Contact instance from the provided data and set the owner_id
    db.add(new_contact)  # Add the new contact to the database session
    await db.commit()  # Commit the changes to the database
    await db.refresh(new_contact)  # Refresh the new contact instance with the latest data from the database
    return new_contact  # Return the newly created contact

async def update_contact(db: AsyncSession, contact_id: int, contact_data: ContactCreate, owner_id: int) -> Optional[Contact]:
    """
    Update a contact in the database based on its ID and owner ID.

    Parameters:
    db (AsyncSession): The database session for asynchronous operations.
    contact_id (int): The ID of the contact to update.
    contact_data (ContactCreate): The updated contact data.
    owner_id (int): The ID of the owner of the contact.

    Returns:
    Optional[Contact]: The updated contact if found and successfully updated, or None if not found.

    Raises:
    Exception: If any error occurs during the database operation.

    Note:
    This function first fetches the contact from the database using the provided contact_id and owner_id.
    If the contact is found, it iterates over the key-value pairs in the contact_data and updates the corresponding attributes of the contact.
    After updating the contact, it commits the changes to the database and refreshes the contact instance with the latest data.
    Finally, it returns the updated contact.
    """
    query = select(Contact).where(Contact.id == contact_id, Contact.owner_id == owner_id)
    result = await db.execute(query)
    contact = result.scalars().first()
    if not contact:
        return None
    for key, value in contact_data.dict().items():
        setattr(contact, key, value)
    await db.commit()
    await db.refresh(contact)
    return contact

async def delete_contact(db: AsyncSession, contact_id: int, owner_id: int) -> Optional[Contact]:
    """
    Delete a contact from the database based on its ID and owner ID.

    Parameters:
    db (AsyncSession): The database session for asynchronous operations.
    contact_id (int): The ID of the contact to delete.
    owner_id (int): The ID of the owner of the contact.

    Returns:
    Optional[Contact]: The deleted contact if found and successfully deleted, or None if not found.

    Raises:
    Exception: If any error occurs during the database operation.
    """
    db_contact = select(Contact).where(Contact.id == contact_id, Contact.owner_id == owner_id)
    result = await db.execute(db_contact)
    contact = result.scalars().first()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact

async def get_upcoming_birthdays(db: AsyncSession, owner_id: int) -> List[Contact]:
    """
    Fetch a list of contacts whose birthdays are within the next week.

    Parameters:
    db (AsyncSession): The database session for asynchronous operations.
    owner_id (int): The ID of the owner of the contacts.

    Returns:
    List[Contact]: A list of contacts whose birthdays are within the next week.

    Note:
    This function calculates the birthdays for the current year and checks if they fall within the next week.
    It fetches all contacts from the database for the specified owner_id and iterates over them to find the upcoming birthdays.
    """
    today = datetime.today()
    next_week = today + timedelta(days=7)

    query = select(Contact).where(Contact.owner_id == owner_id)
    result = await db.execute(query)
    contacts = result.scalars().all()

    upcoming_birthdays = []
    for contact in contacts:
        if contact.birthday:
            birthday_this_year = contact.birthday.replace(year=today.year)
            if today <= birthday_this_year <= next_week:
                upcoming_birthdays.append(contact)

    return upcoming_birthdays