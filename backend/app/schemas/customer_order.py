from typing import Optional, List
from pydantic import BaseModel
import datetime
import uuid

# CustomerOrderItem Schemas
class CustomerOrderItemBase(BaseModel):
    item_number: Optional[int] = None
    test_name: Optional[str] = None
    sample_type: Optional[str] = None
    test_count: int = 1
    norm_method: Optional[str] = None

class CustomerOrderItemCreate(CustomerOrderItemBase):
    pass

class CustomerOrderItem(CustomerOrderItemBase):
    id: int
    customer_order_id: uuid.UUID

    model_config = {"from_attributes": True}

# CustomerOrder Schemas
class CustomerOrderBase(BaseModel):
    date: datetime.date = datetime.date.today()
    client_name: str
    client_direction: Optional[str] = None
    client_ruc: Optional[str] = None
    client_dv: Optional[str] = None
    client_phone: Optional[str] = None
    
    project_name: Optional[str] = None
    project_location: Optional[str] = None
    project_responsable: Optional[str] = None
    project_responsable_phone: Optional[str] = None
    project_responsable_email: Optional[str] = None
    
    observations: Optional[str] = None
    attended_by: Optional[str] = None
    approved_quotation_number: Optional[str] = None

class CustomerOrderCreate(CustomerOrderBase):
    items: List[CustomerOrderItemCreate] = []

class CustomerOrderUpdate(CustomerOrderBase):
    items: Optional[List[CustomerOrderItemCreate]] = None

class CustomerOrder(CustomerOrderBase):
    id: uuid.UUID
    order_number: str
    created_by: Optional[str] = None
    items: List[CustomerOrderItem] = []

    model_config = {"from_attributes": True}
