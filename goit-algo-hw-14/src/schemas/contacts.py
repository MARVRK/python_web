from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional,List

class ContactCreate(BaseModel):
    """
    A class used to represent a contact for creation.

    Attributes
    ----------
    name : str
        The first name of the contact.
    surename : str
        The last name of the contact.
    email : EmailStr
        The email address of the contact.
    phone_number : str
        The phone number of the contact.
    birthday : date
        The birthday of the contact.
    other_info : Optional[str], optional
        Additional information about the contact. The default is None.
    """

    name: str
    surename: str
    email: EmailStr
    phone_number: str
    birthday: date
    other_info: Optional[str] = None

class ContactResponse(BaseModel):
    """
    A class used to represent a contact response.

    Attributes
    ----------
    id : int
        The unique identifier of the contact.
    name : str
        The first name of the contact.
    surename : str
        The last name of the contact.
    email : EmailStr
        The email address of the contact.
    phone_number : str
        The phone number of the contact.
    birthday : date
        The birthday of the contact.
    other_info : Optional[str], optional
        Additional information about the contact. The default is None.

    Methods
    -------
    None

    """

    id: int
    name: str
    surename: str
    email: EmailStr
    phone_number: str
    birthday: date
    other_info: Optional[str] = None

    class Config:
        """
        Configuration settings for the ContactResponse class.

        Attributes
        ----------
        orm_mode : bool
            A flag indicating whether the class is used in ORM mode.

        Methods
        -------
        None

        """

        orm_mode = True

class UpcomingBirthdaysResponse(BaseModel):
    """
    A class used to represent a response for upcoming birthdays.

    Attributes
    ----------
    message : str
        A message indicating the status of the request.
    contacts : List[ContactResponse]
        A list of ContactResponse objects representing the upcoming birthdays.

    Methods
    -------
    None

    """

    message: str
    contacts: List[ContactResponse]