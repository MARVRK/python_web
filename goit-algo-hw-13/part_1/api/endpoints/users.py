from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session

from api.db.models import User
from api.utils.cloudinary import upload_avatar
from api.endpoints.auth import get_current_user
from api.db.session import get_db

router = APIRouter()

@router.post("/avatar")
async def update_avatar(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = upload_avatar(file.file)
    current_user.avatar_url = result["secure_url"]
    db.commit()
    db.refresh(current_user)
    return {"avatar_url": current_user.avatar_url}

