from pydantic import BaseModel, EmailStr
from datetime import date

class ResponseContactModel(BaseModel):
    id: int
    name: str
    surname: str
    phone_number: str
    email: EmailStr
    birthday: date
    other_info: str

    class Config:
        orm_mode = True

class ContactModel(BaseModel):
    name: str
    surname: str
    email: EmailStr
    phone_number: str
    birthday: date
    other_info: str

    class Config:
        orm_mode = True
