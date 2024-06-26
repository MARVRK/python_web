from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool

    class Config:
        orm_mode = True

class RequestEmail(BaseModel):
    email: EmailStr

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"