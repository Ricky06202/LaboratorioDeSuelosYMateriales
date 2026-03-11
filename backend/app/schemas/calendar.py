from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CalendarActivityBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    type: Optional[str] = None
    related_id: Optional[UUID] = None
    color: Optional[str] = None

class CalendarActivityCreate(CalendarActivityBase):
    pass

class CalendarActivityUpdate(CalendarActivityBase):
    title: Optional[str] = None
    start_date: Optional[datetime] = None

class CalendarActivitySchema(CalendarActivityBase):
    id: UUID

    class Config:
        from_attributes = True
