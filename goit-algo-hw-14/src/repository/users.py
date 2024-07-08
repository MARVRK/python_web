from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar
from src.database.db import get_db
from src.entity.models import User
from src.schemas.user import UserCreate


async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a user from the database based on their email.

    Parameters:
    email (str): The email of the user to retrieve.
    db (AsyncSession, optional): The database session. Defaults to Depends(get_db).

    Returns:
    User: The user object if found, otherwise None.

    Note:
    This function uses SQLAlchemy's select statement to query the database.
    It assumes that the User model is defined in the src.entity.models module.
    """
    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user

async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new user in the database.

    Parameters:
    body (UserCreate): The user data to create a new user.
    db (AsyncSession, optional): The database session. Defaults to Depends(get_db).

    Returns:
    User: The newly created user.

    Raises:
    Exception: If there is an error while fetching the avatar from Gravatar.
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as err:
        print(err)

    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def update_token(user: User, token: str | None, db: AsyncSession):
    """
    Updates the refresh token of a user in the database.

    Parameters:
    user (User): The user object for which the refresh token needs to be updated.
    token (str | None): The new refresh token. If None, the refresh token will be set to None.
    db (AsyncSession): The database session.

    Returns:
    None: This function does not return any value.

    Raises:
    None: This function does not raise any exceptions.

    Note:
    This function assumes that the user object exists in the database.
    If the user object does not exist, this function will not raise an error.
    """
    user.refresh_token = token
    await db.commit()
async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
    Marks the user's email as confirmed in the database.

    Parameters:
    email (str): The email of the user to confirm.
    db (AsyncSession): The database session.

    Returns:
    None: This function does not return any value.

    Raises:
    None: This function does not raise any exceptions.

    Note:
    This function assumes that the user's email exists in the database.
    If the email does not exist, this function will not raise an error.
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()

async def update_avatar_url(email: str, url: str | None, db: AsyncSession) -> User:
    """
    Updates the avatar URL of a user in the database.

    Parameters:
    email (str): The email of the user whose avatar URL needs to be updated.
    url (str | None): The new avatar URL. If None, the avatar URL will be set to None.
    db (AsyncSession): The database session.

    Returns:
    User: The updated user object with the new avatar URL.

    Raises:
    None: This function does not raise any exceptions.

    Note:
    This function assumes that the user's email exists in the database.
    If the email does not exist, this function will not raise an error.
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user
