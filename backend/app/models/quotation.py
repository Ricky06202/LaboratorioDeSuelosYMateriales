from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime
from app.db.base_class import Base

class Quotation(Base):
    __tablename__ = "quotations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quotation_number = Column(String, index=True, nullable=False, unique=True)
    year = Column(Integer, default=lambda: datetime.datetime.now().year)
    date = Column(Date, default=datetime.date.today)
    
    # Customer reference
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True)
    
    # Customer order reference (if created from a customer order)
    customer_order_id = Column(UUID(as_uuid=True), ForeignKey("customer_orders.id"), nullable=True)
    
    # Client info
    client_name = Column(String, nullable=False)
    client_ruc = Column(String)
    client_direction = Column(String)
    client_phone = Column(String)
    client_email = Column(String)
    
    # Project info
    project_responsable = Column(String)
    project_ruc = Column(String)
    project_name = Column(String)
    project_location = Column(String)
    
    # Totals and additional costs
    subtotal_amount = Column(Float, default=0.0)
    mobilization_cost = Column(Float, default=0.0)
    viatics_cost = Column(Float, default=0.0)
    total_amount = Column(Float, default=0.0)
    
    note = Column(Text)
    created_by = Column(String) # user who created the quotation

    items = relationship("QuotationItem", back_populates="quotation", cascade="all, delete-orphan")

class QuotationItem(Base):
    __tablename__ = "quotation_items"

    id = Column(Integer, primary_key=True, index=True)
    quotation_id = Column(UUID(as_uuid=True), ForeignKey("quotations.id"), nullable=False)
    
    item_norma = Column(String)
    item_sample = Column(String)
    amount = Column(Integer, default=1)
    description = Column(String)
    unit_price = Column(Float, default=0.0)
    item_note = Column(String)
    total_price = Column(Float, default=0.0)

    quotation = relationship("Quotation", back_populates="items")
