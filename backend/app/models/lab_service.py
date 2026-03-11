from sqlalchemy import Column, String, Float, Text, Integer
from app.db.base_class import Base

class LabService(Base):
    __tablename__ = "lab_services"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    unit_price = Column(Float, default=0.0)
