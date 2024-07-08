from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """
    This class represents a data model for creating a new user.

    Attributes:
    email (EmailStr): The email of the user. Must be a valid email address.
    username (str): The username of the user. Must be a string.
    password (str): The password of the user. Must be a string.
    """

    email: EmailStr
    username: str
    password: str

class UserResponse(BaseModel):
    """
    This class represents a data model for a user response.

    Attributes:
    id (int): The unique identifier of the user.
    email (EmailStr): The email of the user. Must be a valid email address.
    username (str): The username of the user. Must be a string.
    is_active (bool): Indicates whether the user is active or not.

    Methods:
    None

    """

    id: int
    email: EmailStr
    username: str
    is_active: bool

    class Config:
        """
        This inner class provides configuration settings for the UserResponse class.

        Attributes:
        orm_mode (bool): Indicates whether the class is used for ORM (Object-Relational Mapping) operations.

        Methods:
        None

        """

        orm_mode = True

class RequestEmail(BaseModel):
    """
    This class represents a data model for a request email.

    Attributes:
    email (EmailStr): The email of the user. Must be a valid email address.

    Methods:
    None

    """

    email: EmailStr
    """
    This attribute represents the email of the user. It is a required field and must be a valid email address.
    """

class TokenSchema(BaseModel):
    """
    This class represents a schema for JWT tokens.

    Attributes:
    access_token (str): The access token for authentication.
    refresh_token (str): The refresh token for obtaining a new access token.
    token_type (str): The type of token. Default is "bearer".
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"