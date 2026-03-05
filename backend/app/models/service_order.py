from sqlalchemy import Column, String, Integer, Float, Date, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime
from app.db.base_class import Base

class ServiceOrder(Base):
    __tablename__ = "service_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_number = Column(String, index=True, nullable=False, unique=True)
    year = Column(Integer, default=lambda: datetime.datetime.now().year)
    date = Column(Date, default=datetime.date.today)
    
    # Client info
    client_name = Column(String, nullable=False)
    client_ruc = Column(String)
    client_dv = Column(String) # D.V.
    quotation_ref = Column(String) # Cotización aprobada LSMCH No.
    client_phone = Column(String)
    client_email = Column(String)
    client_direction = Column(String)
    
    # Project info
    project_name = Column(String)
    project_location = Column(String)
    project_responsable = Column(String)
    project_phone = Column(String) # Celular
    
    # Service type
    service_type_ensayos = Column(Boolean, default=True)
    service_type_muestreo = Column(Boolean, default=False)
    
    # Performed by
    performed_by_laboratory = Column(Boolean, default=True)
    performed_by_client = Column(Boolean, default=False)
    performed_by_inspection = Column(Boolean, default=False)
    
    # Details
    item_description = Column(Text)
    methodology = Column(Text)
    
    # Subcontraction
    subcontraction = Column(Boolean, default=False)
    subcontraction_details = Column(String)
    
    # Conformity
    request_declaration_conformity = Column(Boolean, default=False)
    declaration_specification = Column(String)
    
    # Decision rule
    decision_rule_not_applicable = Column(Boolean, default=True)
    decision_rule_client_agreed = Column(Boolean, default=False)
    decision_rule_inherent = Column(Boolean, default=False)
    
    # Client deviation
    client_deviation = Column(Boolean, default=False)
    deviation_details = Column(String)
    
    observations = Column(Text)
    sample_conservation_time = Column(Integer, default=30)
    
    # Costs
    total_cost = Column(Float, default=0.0)
    paid_100_percent = Column(Boolean, default=False)
    service_sale_receipt_number = Column(String)
    
    # Relates to Inform
    relates_to_inform = Column(String) # Informe LSMCH No
    number_of_informs = Column(Integer, default=1)
    
    # Support
    support_institutional = Column(Boolean, default=False)
    related_document = Column(String)
    
    attended_by = Column(String)
    applicant_name = Column(String)
    applicant_id_number = Column(String) # No. de Cédula
    created_by = Column(String)
