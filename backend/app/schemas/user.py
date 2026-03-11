from typing import Optional, List
from pydantic import BaseModel, EmailStr

class Permission(BaseModel):
    id: int
    name: str
    code: str

    class Config:
        from_attributes = True

class Role(BaseModel):
    id: int
    name: str
    permissions: List[Permission] = []

    class Config:
        from_attributes = True

class RoleCreate(BaseModel):
    name: str
    permission_ids: List[int] = []

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    permission_ids: Optional[List[int]] = None

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    full_name: Optional[str] = None

class UserCreate(UserBase):
    email: EmailStr
    password: str
    role_ids: List[int] = []

class UserUpdate(UserBase):
    password: Optional[str] = None
    role_ids: Optional[List[int]] = None

class User(UserBase):
    id: Optional[int] = None
    roles: List[Role] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None
    roles: List[str] = []
    
    model_config = {
        "extra": "allow"
    }
