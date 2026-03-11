from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime
from app.db.base_class import Base

class CalendarActivity(Base):
    __tablename__ = "calendar_activities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text)
    start_date = Column(DateTime, default=datetime.datetime.utcnow)
    end_date = Column(DateTime)
    type = Column(String)  # 'order', 'maintenance', 'field_trip', 'manual'
    related_id = Column(UUID(as_uuid=True), nullable=True) # ID of related CustomerOrder or Equipment
    color = Column(String) # For UI display
