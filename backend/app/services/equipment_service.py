from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta
from typing import List, Tuple
from app.models.equipment import Equipo, Calibracion, EquipoStatus
from app.schemas.equipment import EquipoCreate, EquipoUpdate, CalibracionCreate

class EquipmentService:
    @staticmethod
    def get_equipos(db: Session, skip: int = 0, limit: int = 10, search: str = None, estado: str = None) -> Tuple[List[Equipo], int]:
        query = db.query(Equipo)
        if search:
            query = query.filter(
                or_(
                    Equipo.nombre.ilike(f"%{search}%"),
                    Equipo.numero_serie.ilike(f"%{search}%")
                )
            )
        if estado:
            query = query.filter(Equipo.estado == estado)
        total = query.count()
        return query.offset(skip).limit(limit).all(), total

    @staticmethod
    def get_equipo(db: Session, equipo_id: str):
        return db.query(Equipo).filter(Equipo.id == equipo_id).first()

    @staticmethod
    def create_equipo(db: Session, equipo: EquipoCreate):
        db_obj = Equipo(**equipo.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update_equipo(db: Session, equipo_id: str, equipo: EquipoUpdate):
        db_obj = db.query(Equipo).filter(Equipo.id == equipo_id).first()
        if not db_obj:
            return None
        
        obj_data = equipo.model_dump(exclude_unset=True)
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def create_calibracion(db: Session, calibracion: CalibracionCreate):
        db_obj = Calibracion(**calibracion.model_dump())
        db.add(db_obj)
        
        # Update fecha_proxima_calibracion in the parent Equipo
        equipo_obj = db.query(Equipo).filter(Equipo.id == calibracion.equipo_id).first()
        if equipo_obj:
            # Only update if the new expiration is further in the future or if it's currently null
            if not equipo_obj.fecha_proxima_calibracion or calibracion.fecha_vencimiento > equipo_obj.fecha_proxima_calibracion:
                equipo_obj.fecha_proxima_calibracion = calibracion.fecha_vencimiento
                
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def get_calibration_alerts(db: Session):
        """
        Returns equipment whose next calibration expires in less than 30 days or is already expired.
        Optimized to use native PostgreSQL date functions against the new column.
        """
        warning_date = func.current_date() + timedelta(days=30)
        
        alerts = db.query(Equipo).filter(
            Equipo.fecha_proxima_calibracion != None,
            Equipo.fecha_proxima_calibracion <= warning_date
        ).all()
        
        return alerts

    @staticmethod
    def delete_equipo(db: Session, equipo_id: str):
        db_obj = db.query(Equipo).filter(Equipo.id == equipo_id).first()
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj

equipment_service = EquipmentService()
