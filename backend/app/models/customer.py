from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base_class import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, index=True)
    ruc = Column(String, unique=True, index=True)
    dv = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(Text)
