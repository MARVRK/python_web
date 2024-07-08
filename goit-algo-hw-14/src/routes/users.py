import pickle
import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.entity.models import User
from src.schemas.user import UserResponse
from src.services.auth import auth_service
from src.conf.config import config
from src.repository import users as repositories_users
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])
cloudinary.config(
    cloud_name=config.CLOUDINARY_CLOUD_NAME,
    api_key=config.CLOUDINARY_API_KEY,
    api_secret=config.CLOUDINARY_API_SECRET,
    secure=True,
)


@router.get(
    "/me",
    response_model=UserResponse,
    dependencies=[Depends(RateLimiter(times=1, seconds=20))],
)
async def get_current_user(user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve the current user's information.

    This function is a FastAPI endpoint that retrieves the current user's information.
    It uses the `auth_service.get_current_user` function to authenticate the user and
    retrieve their details from the database. The retrieved user information is then
    returned as a response.

    Parameters:
    user (User): The authenticated user object. This parameter is obtained using the
                 `auth_service.get_current_user` function and is automatically
                 injected by FastAPI.

    Returns:
    UserResponse: The response containing the current user's information. This response
                  is serialized using the `UserResponse` model.

    Raises:
    None
    """
    return user


@router.patch(
    "/avatar",
    response_model=UserResponse,
    dependencies=[Depends(RateLimiter(times=1, seconds=20))],
)

async def get_current_user(
    file: UploadFile = File(),
    user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Update the current user's avatar.

    This function is a FastAPI endpoint that retrieves the current user's information.
    It uses the `auth_service.get_current_user` function to authenticate the user and
    retrieve their details from the database. The retrieved user information is then
    returned as a response.

    Parameters:
    file (UploadFile): The uploaded image file. This parameter is obtained using the
                       `File()` FastAPI dependency.
    user (User): The authenticated user object. This parameter is obtained using the
                 `auth_service.get_current_user` function and is automatically
                 injected by FastAPI.
    db (AsyncSession): The database session object. This parameter is obtained using
                       the `get_db` FastAPI dependency and is automatically
                       injected by FastAPI.

    Returns:
    UserResponse: The response containing the updated user's information. This response
                  is serialized using the `UserResponse` model.

    Raises:
    None
    """
    public_id = f"HM13/{user.email}"
    res = cloudinary.uploader.upload(file.file, public_id=public_id, owerite=True)
    res_url = cloudinary.CloudinaryImage(public_id).build_url(
        width=250, height=250, crop="fill", version=res.get("version"))
    user = await repositories_users.update_avatar_url(user.email, res_url, db)
    auth_service.cache.set(user.email, pickle.dumps(user))
    auth_service.cache.expire(user.email, 300)
    return user

@router.patch("/api/users/testing-avatar-upload")
async def update_avatar():
    """
    This function is used to update the avatar of a user.

    The function simulates a cloud service interaction to update the avatar.
    It checks the validity of the cloud name before proceeding with the update.

    Parameters:
    None

    Returns:
    dict: A dictionary containing a success message if the avatar is updated successfully.
          If an error occurs during the update, an HTTPException is raised.

    Raises:
    HTTPException: If an error occurs during the update, an HTTPException is raised
                   with a status code of 500 and a detail message indicating the error.
    """
    try:
        # Your code to update avatar
        cloud_name = "marv"
        logger.info(f"Updating avatar for cloud name: {cloud_name}")

        # Simulate cloud service interaction
        if cloud_name != "expected_cloud_name":
            raise ValueError("Invalid cloud name")

        return {
            "message": "Avatar updated successfully"}
    except Exception as e:
        logger.error(f"Error updating avatar: {e}")
        raise HTTPException(status_code=500,detail="Internal Server Error")
