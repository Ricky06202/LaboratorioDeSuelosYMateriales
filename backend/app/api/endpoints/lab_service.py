from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.services.lab_service_service import lab_service_service
from app.schemas.lab_service import LabServiceSchema, LabServiceCreate, LabServiceUpdate
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[LabServiceSchema])
def read_services(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    services, _ = lab_service_service.get_services(db, skip=skip, limit=limit, search=search)
    return services

@router.post("/", response_model=LabServiceSchema)
def create_service(
    *,
    db: Session = Depends(deps.get_db),
    service_in: LabServiceCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return lab_service_service.create_service(db, service=service_in)

@router.get("/{service_id}", response_model=LabServiceSchema)
def read_service(
    *,
    db: Session = Depends(deps.get_db),
    service_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    service = lab_service_service.get_service(db, service_id=service_id)
    if not service:
        raise HTTPException(status_code=404, detail="LabService not found")
    return service

@router.put("/{service_id}", response_model=LabServiceSchema)
def update_service(
    *,
    db: Session = Depends(deps.get_db),
    service_id: int,
    service_in: LabServiceUpdate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    service = lab_service_service.get_service(db, service_id=service_id)
    if not service:
        raise HTTPException(status_code=404, detail="LabService not found")
    return lab_service_service.update_service(db, service_id=service_id, service=service_in)

@router.delete("/{service_id}", response_model=LabServiceSchema)
def delete_service(
    *,
    db: Session = Depends(deps.get_db),
    service_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    service = lab_service_service.get_service(db, service_id=service_id)
    if not service:
        raise HTTPException(status_code=404, detail="LabService not found")
    return lab_service_service.delete_service(db, service_id=service_id)
