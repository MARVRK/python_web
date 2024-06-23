from asyncio.log import logger

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from api.core.security import create_access_token, verify_password, get_password_hash
from api.schemas.token import Token
from api.schemas.user import UserCreate, UserResponse
from api.db.models import User
from api.db.session import get_db
from api.utils.email import send_verification_email, \
    create_verification_token, \
    create_reset_token, \
    SECRET_KEY, \
    ALGORITHM
from api.core.config import settings
from jose import jwt, JWTError



router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register", response_model=Token, status_code=201)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Registering user: {user.email}")
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            logger.error(f"User with email {user.email} already exists")
            raise HTTPException(status_code=409, detail="Email already exists")

        hashed_password = get_password_hash(user.password)
        new_user = User(email=user.email, hashed_password=hashed_password, is_active=True)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"User {user.email} registered successfully")

        verification_token = create_verification_token(user.email)
        send_verification_email(user.email, verification_token)

        access_token = create_access_token(data={"sub": new_user.email})
        logger.info(f"Access token created for user: {user.email}")
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Error registering user: {e}", exc_info=True)
        raise


@router.get("/get_user", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload["sub"]
        db_user = db.query(User).filter(User.email == email).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/verify-email")
async def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload["sub"]
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.is_active = True
        db.commit()
        return {"message": "Email verified successfully"}
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")


@router.post("/reset-password")
async def reset_password(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    reset_token = create_reset_token(email)
    await send_verification_email(email, reset_token)
    return {"message": "Password reset email sent"}


@router.post("/reset-password/confirm")
async def confirm_reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload["sub"]
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.hashed_password = get_password_hash(new_password)
        db.commit()
        return {"message": "Password reset successfully"}
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
