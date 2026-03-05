from sqlalchemy import Column, String, Integer, Date, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime
from app.db.base_class import Base

class CustomerOrder(Base):
    __tablename__ = "customer_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_number = Column(String, index=True, nullable=False, unique=True)
    date = Column(Date, default=datetime.date.today)
    
    # Client info
    client_name = Column(String, nullable=False)
    client_direction = Column(String)
    client_ruc = Column(String)
    client_dv = Column(String)
    client_phone = Column(String)
    
    # Project info
    project_name = Column(String)
    project_location = Column(String)
    project_responsable = Column(String)
    project_responsable_phone = Column(String)
    project_responsable_email = Column(String)
    
    # Observations
    observations = Column(Text)
    
    # Internal info
    attended_by = Column(String)
    approved_quotation_number = Column(String)
    
    created_by = Column(String) # user who created the order

    items = relationship("CustomerOrderItem", back_populates="customer_order", cascade="all, delete-orphan")

class CustomerOrderItem(Base):
    __tablename__ = "customer_order_items"

    id = Column(Integer, primary_key=True, index=True)
    customer_order_id = Column(UUID(as_uuid=True), ForeignKey("customer_orders.id"), nullable=False)
    
    item_number = Column(Integer)
    test_name = Column(String)
    sample_type = Column(String)
    test_count = Column(Integer, default=1)
    norm_method = Column(String)

    customer_order = relationship("CustomerOrder", back_populates="items")
