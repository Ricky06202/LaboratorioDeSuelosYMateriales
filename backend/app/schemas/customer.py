from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID

class CustomerBase(BaseModel):
    name: str
    ruc: Optional[str] = None
    dv: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    name: Optional[str] = None

class CustomerSchema(CustomerBase):
    id: UUID

    class Config:
        from_attributes = True
