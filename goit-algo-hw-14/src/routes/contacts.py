from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from typing import List, Optional
from src.database.db import get_db
from src.entity.models import User
from src.schemas.contacts import ContactResponse, \
    ContactCreate, \
    UpcomingBirthdaysResponse
from src.repository import contacts as contact_repo
from src.services.auth import auth_service

router = APIRouter()

@router.post("/contacts", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(contact: ContactCreate, db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)):
    """
    Creates a new contact.

    Parameters:
    contact (ContactCreate): The contact data to be created.
    db (AsyncSession): The database session.
    current_user (User): The current authenticated user.

    Returns:
    ContactResponse: The newly created contact.

    Raises:
    HTTPException: If the contact could not be created.
    """
    new_contact = await contact_repo.create_contact(db, contact, current_user.id)
    return new_contact

@router.get("/contact/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieves a contact by its ID.

    Parameters:
    contact_id (int): The ID of the contact to retrieve.
    db (Session): The database session.
    current_user (User): The current authenticated user.

    Returns:
    ContactResponse: The retrieved contact.

    Raises:
    HTTPException: If the contact is not found.
    """
    contact = await contact_repo.get_contact_by_id(db, contact_id, current_user.id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.get("/contacts", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user), name: Optional[str] = Query(None), surename: Optional[str] = Query(None), email: Optional[str] = Query(None)):
    """
    Retrieves a list of contacts based on the provided filters.

    Parameters:
    skip (int): The number of contacts to skip. Default is 0.
    limit (int): The maximum number of contacts to retrieve. Default is 10.
    db (Session): The database session.
    current_user (User): The current authenticated user.
    name (Optional[str]): The name filter. Default is None.
    surename (Optional[str]): The surename filter. Default is None.
    email (Optional[str]): The email filter. Default is None.

    Returns:
    List[ContactResponse]: A list of retrieved contacts.

    Raises:
    None
    """
    contacts = await contact_repo.get_contacts(db, current_user.id, skip, limit, name, surename, email)
    return contacts

@router.put("/contacts/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, contact: ContactCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Updates an existing contact with the provided data.

    Parameters:
    contact_id (int): The ID of the contact to update.
    contact (ContactCreate): The updated contact data.
    db (AsyncSession): The database session.
    current_user (User): The current authenticated user.

    Returns:
    ContactResponse: The updated contact.

    Raises:
    HTTPException: If the contact is not found.
    """
    updated_contact = await contact_repo.update_contact(db, contact_id, contact, current_user.id)
    if not updated_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact

@router.delete("/contacts/{contact_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Deletes a contact by its ID.

    Parameters:
    contact_id (int): The ID of the contact to delete.
    db (AsyncSession): The database session.
    current_user (User): The current authenticated user.

    Returns:
    None

    Raises:
    HTTPException: If the contact is not found.
    """
    contact = await contact_repo.delete_contact(db, contact_id, current_user.id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.get("/contacts/upcoming_birthdays", response_model=List[UpcomingBirthdaysResponse])
async def upcoming_birthdays(db: AsyncSession = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieves a list of upcoming birthdays for the current user.

    Parameters:
    db (AsyncSession): The database session.
    current_user (User): The current authenticated user.

    Returns:
    List[UpcomingBirthdaysResponse]: A list of upcoming birthdays. Each item in the list contains the contact's name,
    surename, and date of birth.

    Raises:
    None
    """
    upcoming_birthdays = await contact_repo.get_upcoming_birthdays(db, current_user.id)
    return upcoming_birthdays

