from datetime import datetime, \
    timedelta

from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.param_functions import Query
from sqlalchemy.orm import Session
from typing import Optional, \
    List

from api.core.security import get_password_hash, verify_password
from api.endpoints.auth import get_current_user
from api.db.models import User, Contact
from api.schemas.contact import ContactCreate, ContactResponse
from api.db.session import get_db
from slowapi.extension import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/contacts", response_model=ContactResponse, status_code=201)

async def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_contact = Contact(**contact.dict(), owner_id=current_user.id)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

@router.get("/contacts/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == current_user.id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.get("/contacts", response_model=List[ContactResponse])
async def read_contacts(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        name: Optional[str] = Query(None),
        surename: Optional[str] = Query(None),
        email: Optional[str] = Query(None)
):
    query = db.query(Contact).filter(Contact.owner_id == current_user.id)

    if name:
        query = query.filter(Contact.name.ilike(f"%{name}%"))
    if surename:
        query = query.filter(Contact.surename.ilike(f"%{surename}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))

    contacts = query.offset(skip).limit(limit).all()
    return contacts


@router.put("/contacts/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == current_user.id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@router.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == current_user.id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return


@router.get("/contacts/upcoming_birthdays", response_model=List[ContactResponse])
async def upcoming_birthdays(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    today = datetime.today().date()
    next_week = today + timedelta(days=7)
    contacts = db.query(Contact).filter(Contact.owner_id == current_user.id).all()

    upcoming_birthdays = []
    for contact in contacts:
        birthday_this_year = contact.birthday.replace(year=today.year)
        if today <= birthday_this_year <= next_week:
            upcoming_birthdays.append(contact)

    return upcoming_birthdays

