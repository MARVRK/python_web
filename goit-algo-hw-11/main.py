from fastapi import FastAPI, Depends, HTTPException, Query, Path, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import text, extract, and_
from datetime import datetime, time, timedelta, date
import time
from typing import List
from sqlalchemy.exc import IntegrityError
from models import ResponseContactModel, ContactModel
from db import get_db, AddressBook

app = FastAPI()


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")

@app.get("/contacts", response_model=List[ResponseContactModel])
async def show_contacts(skip: int = 0, limit: int = Query(default=5, le=20, ge=5), db: Session = Depends(get_db)):
    contacts = db.query(AddressBook).offset(skip).limit(limit).all()
    return contacts

@app.get("/contacts/search", response_model=List[ResponseContactModel])
async def search_contacts(
    name: str = Query(None),
    surname: str = Query(None),
    email: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(AddressBook)
    if name:
        query = query.filter(AddressBook.name.ilike(f"%{name}%"))
    if surname:
        query = query.filter(AddressBook.surname.ilike(f"%{surname}%"))
    if email:
        query = query.filter(AddressBook.email.ilike(f"%{email}%"))

    results = query.all()
    return results

@app.get("/contacts/upcoming_birthdays", response_model=List[ResponseContactModel])
async def upcoming_birthdays(db: Session = Depends(get_db)):
    today = datetime.today().date()
    next_week = today + timedelta(days=7)
    contacts = db.query(AddressBook).filter(
        and_(
            extract('month', AddressBook.birthday) == today.month,
            extract('day', AddressBook.birthday) >= today.day
        ) | and_(
            extract('month', AddressBook.birthday) == next_week.month,
            extract('day', AddressBook.birthday) <= next_week.day
        )
    ).all()
    return contacts

@app.get("/contacts/{contact_id}", response_model=ResponseContactModel)
async def show_contact(contact_id: int = Path(description="The ID of the contact to get", gt=0), db: Session = Depends(get_db)):
    contact = db.query(AddressBook).filter(AddressBook.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@app.post("/contacts", response_model=ResponseContactModel)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    new_contact = AddressBook(
        name=body.name,
        surname=body.surname,
        email=body.email,
        phone_number=body.phone_number,
        birthday=body.birthday,
        other_info=body.other_info
    )
    try:
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        return new_contact
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contact with this email already exists")

@app.put("/contacts/{contact_id}", response_model=ResponseContactModel)
async def update_contact(contact_id: int, body: ContactModel, db: Session = Depends(get_db)):
    contact = db.query(AddressBook).filter(AddressBook.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    
    contact.name = body.name
    contact.surname = body.surname
    contact.email = body.email
    contact.phone_number = body.phone_number
    contact.birthday = body.birthday
    contact.other_info = body.other_info

    db.commit()
    db.refresh(contact)
    return contact

@app.delete("/contacts/{contact_id}", response_model=ResponseContactModel)
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(AddressBook).filter(AddressBook.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    db.delete(contact)
    db.commit()
    return contact

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
