from typing import Optional, List
from pydantic import BaseModel, EmailStr

class Role(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class RoleCreate(BaseModel):
    name: str

class RoleUpdate(BaseModel):
    name: str

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    full_name: Optional[str] = None
    role_id: Optional[int] = None

class UserCreate(UserBase):
    email: EmailStr
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: Optional[int] = None
    role_name: Optional[str] = None

    class Config:
        from_attributes = True

class UserRole(User):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None
    
    model_config = {
        "extra": "allow"
    }
