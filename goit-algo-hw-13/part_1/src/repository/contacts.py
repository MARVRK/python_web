from sqlalchemy.orm import Session
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
    query = select(Contact).where(Contact.id == contact_id, Contact.owner_id == owner_id)
    result = await db.execute(query)
    return result.scalars().first()

async def create_contact(db: AsyncSession, contact: ContactCreate, user_id: int) -> Contact:
    new_contact = Contact(**contact.dict(), owner_id=user_id)
    db.add(new_contact)
    await db.commit()
    await db.refresh(new_contact)
    return new_contact

async def update_contact(db: AsyncSession, contact_id: int, contact_data: ContactCreate, owner_id: int) -> Optional[Contact]:
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
    db_contact = select(Contact).where(Contact.id == contact_id, Contact.owner_id == owner_id)
    result = await db.execute(db_contact)
    contact = result.scalars().first()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact

async def get_upcoming_birthdays(db: AsyncSession, owner_id: int) -> List[Contact]:
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