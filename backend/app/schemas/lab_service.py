from typing import Optional
from pydantic import BaseModel

class LabServiceBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    unit_price: float = 0.0

class LabServiceCreate(LabServiceBase):
    pass

class LabServiceUpdate(LabServiceBase):
    code: Optional[str] = None
    name: Optional[str] = None

class LabServiceSchema(LabServiceBase):
    id: int

    class Config:
        from_attributes = True
