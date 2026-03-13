from typing import Optional, List
from pydantic import BaseModel, computed_field
import datetime
import uuid

# QuotationItem Schemas
class QuotationItemBase(BaseModel):
    item_norma: Optional[str] = None
    item_sample: Optional[str] = None
    amount: int = 1
    description: Optional[str] = None
    unit_price: float = 0.0
    item_note: Optional[str] = None

class QuotationItemCreate(QuotationItemBase):
    pass

class QuotationItemUpdate(QuotationItemBase):
    pass

class QuotationItemInDBBase(QuotationItemBase):
    id: int
    quotation_id: uuid.UUID
    total_price: float

    model_config = {"from_attributes": True}

class QuotationItem(QuotationItemInDBBase):
    pass

# Quotation Schemas
class QuotationBase(BaseModel):
    client_name: str
    client_ruc: Optional[str] = None
    client_direction: Optional[str] = None
    client_phone: Optional[str] = None
    client_email: Optional[str] = None
    
    project_responsable: Optional[str] = None
    project_ruc: Optional[str] = None
    project_name: Optional[str] = None
    project_location: Optional[str] = None
    
    mobilization_cost: float = 0.0
    viatics_cost: float = 0.0
    note: Optional[str] = None

class QuotationCreate(QuotationBase):
    customer_id: Optional[uuid.UUID] = None
    customer_order_id: Optional[uuid.UUID] = None
    items: List[QuotationItemCreate] = []

class QuotationUpdate(QuotationBase):
    items: Optional[List[QuotationItemCreate]] = None

class QuotationInDBBase(QuotationBase):
    id: uuid.UUID
    quotation_number: str
    year: int
    date: datetime.date
    customer_order_id: Optional[uuid.UUID] = None
    created_by: Optional[str] = None
    subtotal_amount: float
    total_amount: float
    items: List[QuotationItem] = []

    model_config = {"from_attributes": True}

class Quotation(QuotationInDBBase):
    pass

class QuotationInDB(QuotationInDBBase):
    pass
