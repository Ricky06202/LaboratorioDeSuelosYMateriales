from typing import Optional
from pydantic import BaseModel
import datetime
import uuid

class ServiceOrderBase(BaseModel):
    client_name: str
    client_ruc: Optional[str] = None
    client_phone: Optional[str] = None
    client_email: Optional[str] = None
    client_direction: Optional[str] = None
    
    project_name: Optional[str] = None
    project_location: Optional[str] = None
    project_responsable: Optional[str] = None
    project_phone: Optional[str] = None
    
    service_type_ensayos: bool = True
    service_type_muestreo: bool = False
    
    performed_by_laboratory: bool = True
    performed_by_client: bool = False
    performed_by_inspection: bool = False
    
    item_description: Optional[str] = None
    methodology: Optional[str] = None
    
    subcontraction: bool = False
    subcontraction_details: Optional[str] = None
    
    request_declaration_conformity: bool = False
    declaration_specification: Optional[str] = None
    
    decision_rule_not_applicable: bool = True
    decision_rule_client_agreed: bool = False
    decision_rule_inherent: bool = False
    
    client_deviation: bool = False
    deviation_details: Optional[str] = None
    
    observations: Optional[str] = None
    sample_conservation_time: int = 30
    
    total_cost: float = 0.0
    paid_100_percent: bool = False
    service_sale_receipt_number: Optional[str] = None
    
    relates_to_inform: Optional[str] = None
    number_of_informs: int = 1
    
    support_institutional: bool = False
    related_document: Optional[str] = None
    
    attended_by: Optional[str] = None
    applicant_name: Optional[str] = None

class ServiceOrderCreate(ServiceOrderBase):
    pass

class ServiceOrderUpdate(ServiceOrderBase):
    pass

class ServiceOrderInDBBase(ServiceOrderBase):
    id: uuid.UUID
    order_number: str
    year: int
    date: datetime.date
    created_by: Optional[str] = None

    model_config = {"from_attributes": True}

class ServiceOrder(ServiceOrderInDBBase):
    pass

class ServiceOrderInDB(ServiceOrderInDBBase):
    pass
