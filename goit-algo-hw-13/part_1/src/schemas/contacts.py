from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional,List

class ContactCreate(BaseModel):
    name: str
    surename: str
    email: EmailStr
    phone_number: str
    birthday: date
    other_info: Optional[str] = None

class ContactResponse(BaseModel):
    id: int
    name: str
    surename: str
    email: EmailStr
    phone_number: str
    birthday: date
    other_info: Optional[str] = None

    class Config:
        orm_mode = True

class MessageResponse(BaseModel):
    message: str


class UpcomingBirthdaysResponse(BaseModel):
    message: str
    contacts: List[ContactResponse]