from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    contacts = relationship("Contact", back_populates="owner")

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surename = Column(String, index=True)
    email = Column(String, index=True)
    phone_number = Column(String, index=True)
    birthday = Column(Date)
    other_info = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="contacts")

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class RefreshToken(BaseModel):
    refresh_token: str
    token_type: str

class ContactCreate(BaseModel):
    name: str
    surename: str
    email: str
    phone_number: str
    birthday: date
    other_info: Optional[str] = None

class ContactResponse(BaseModel):
    id: int
    name: str
    surename: str
    email: str
    phone_number: str
    birthday: date
    other_info: Optional[str] = None

    class Config:
        orm_mode = True
