from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Tuple
from app.models.lab_service import LabService
from app.schemas.lab_service import LabServiceCreate, LabServiceUpdate

class LabServiceService:
    @staticmethod
    def get_services(db: Session, skip: int = 0, limit: int = 100, search: str = None) -> Tuple[List[LabService], int]:
        query = db.query(LabService)
        if search:
            query = query.filter(
                or_(
                    LabService.name.ilike(f"%{search}%"),
                    LabService.code.ilike(f"%{search}%")
                )
            )
        total = query.count()
        return query.offset(skip).limit(limit).all(), total

    @staticmethod
    def get_service(db: Session, service_id: int):
        return db.query(LabService).filter(LabService.id == service_id).first()

    @staticmethod
    def create_service(db: Session, service: LabServiceCreate):
        db_obj = LabService(**service.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update_service(db: Session, service_id: int, service: LabServiceUpdate):
        db_obj = db.query(LabService).filter(LabService.id == service_id).first()
        if not db_obj:
            return None
        
        obj_data = service.model_dump(exclude_unset=True)
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def delete_service(db: Session, service_id: int):
        db_obj = db.query(LabService).filter(LabService.id == service_id).first()
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj

lab_service_service = LabServiceService()
