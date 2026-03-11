from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Tuple
from app.models.calendar import CalendarActivity
from app.schemas.calendar import CalendarActivityCreate, CalendarActivityUpdate

class CalendarService:
    @staticmethod
    def get_activities(db: Session, start: datetime = None, end: datetime = None) -> List[CalendarActivity]:
        query = db.query(CalendarActivity)
        if start:
            query = query.filter(CalendarActivity.start_date >= start)
        if end:
            query = query.filter(CalendarActivity.start_date <= end)
        return query.all()

    @staticmethod
    def create_activity(db: Session, activity: CalendarActivityCreate):
        db_obj = CalendarActivity(**activity.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update_activity(db: Session, activity_id: str, activity: CalendarActivityUpdate):
        db_obj = db.query(CalendarActivity).filter(CalendarActivity.id == activity_id).first()
        if not db_obj:
            return None
        
        obj_data = activity.model_dump(exclude_unset=True)
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def delete_activity(db: Session, activity_id: str):
        db_obj = db.query(CalendarActivity).filter(CalendarActivity.id == activity_id).first()
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj

calendar_service = CalendarService()
