from aiohttp.web_fileresponse import FileResponse
from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import users as repositories_users
from src.schemas.user import UserCreate, UserResponse, RequestEmail, TokenSchema
from src.services.auth import auth_service
from src.services.email import send_email

router = APIRouter(prefix='/auth', tags=['auth'])
get_refresh_token = HTTPBearer()

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserCreate, bt: BackgroundTasks, request: Request, db: AsyncSession = Depends(get_db)):
    """
    Registers a new user.

    Parameters:
    - body (UserCreate): The user data to be registered.
    - bt (BackgroundTasks): FastAPI's BackgroundTasks instance for sending emails asynchronously.
    - request (Request): FastAPI's Request instance to get the base URL.
    - db (AsyncSession): SQLAlchemy's AsyncSession instance for database operations.

    Returns:
    - UserResponse: The newly created user's data.

    Raises:
    - HTTPException: If the email already exists in the database.
    """
    exist_user = await repositories_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repositories_users.create_user(body, db)
    bt.add_task(send_email, new_user.email, new_user.username, str(request.base_url))
    return new_user

@router.post("/login", response_model=TokenSchema)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    Authenticates a user and generates JWT tokens.

    Parameters:
    - body (OAuth2PasswordRequestForm): The username and password provided by the user.
    - db (AsyncSession): The SQLAlchemy AsyncSession instance for database operations.

    Returns:
    - TokenSchema: A dictionary containing the access token, refresh token, and token type.

    Raises:
    - HTTPException: If the email is not found in the database.
    - HTTPException: If the email is not confirmed.
    - HTTPException: If the provided password does not match the user's password.
    """
    user = await repositories_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repositories_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get('/refresh_token', response_model=TokenSchema)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(get_refresh_token),
                        db: AsyncSession = Depends(get_db)):
    """
    Refreshes the access token using the provided refresh token.

    Parameters:
    - credentials (HTTPAuthorizationCredentials): The refresh token provided by the user.
    - db (AsyncSession): The SQLAlchemy AsyncSession instance for database operations.

    Returns:
    - TokenSchema: A dictionary containing the new access token, refresh token, and token type.

    Raises:
    - HTTPException: If the provided refresh token is invalid.
    """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repositories_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repositories_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repositories_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: AsyncSession = Depends(get_db)):
    """
    Verifies the user's email by decoding the token and updating the user's status in the database.

    Parameters:
    - token (str): The token sent to the user's email for email verification.
    - db (AsyncSession): The SQLAlchemy AsyncSession instance for database operations.

    Returns:
    - dict: A dictionary containing a message indicating the status of the email confirmation.

    Raises:
    - HTTPException: If the provided token is invalid or the user does not exist in the database.
    """
    email = await auth_service.get_email_from_token(token)
    user = await repositories_users.get_user_by_email(email, db)

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")

    if user.confirmed:
        return {"message": "Your email is already confirmed"}

    await repositories_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}

@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: AsyncSession = Depends(get_db)):
    """
    Sends a confirmation email to the user if their email is not already confirmed.

    Parameters:
    - body (RequestEmail): The email address of the user to be confirmed.
    - background_tasks (BackgroundTasks): FastAPI's BackgroundTasks instance for sending emails asynchronously.
    - request (Request): FastAPI's Request instance to get the base URL.
    - db (AsyncSession): SQLAlchemy's AsyncSession instance for database operations.

    Returns:
    - dict: A dictionary containing a message indicating whether the email was sent for confirmation.

    Raises:
    - None
    """
    user = await repositories_users.get_user_by_email(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email, user.email, user.username, str(request.base_url))
    return {"message": "Check your email for confirmation."}
