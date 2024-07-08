from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """
    This class represents a user in the application.

    Attributes:
    id (int): The unique identifier of the user.
    email (str): The email of the user.
    username (str): The username of the user.
    password (str): The password of the user.
    avatar (str): The avatar of the user.
    confirmed (bool): Indicates whether the user's email is confirmed.
    is_active (bool): Indicates whether the user is active.
    contacts (list): A list of contacts associated with the user.

    Methods:
    None
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, index=True)
    password = Column(String)
    avatar = Column(String,nullable=True)
    confirmed = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    contacts = relationship("Contact", back_populates="owner")

class Contact(Base):
    """
    This class represents a contact associated with a user.

    Attributes:
    id (int): The unique identifier of the contact.
    name (str): The name of the contact.
    surename (str): The surename of the contact.
    email (str): The email of the contact.
    phone_number (str): The phone number of the contact.
    birthday (Date): The birthday of the contact.
    other_info (str): Additional information about the contact.
    owner_id (int): The id of the user who owns this contact.
    owner (User): The user who owns this contact.

    Methods:
    None
    """

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
