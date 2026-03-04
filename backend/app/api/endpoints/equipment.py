from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.api import deps
from app.schemas.equipment import Equipo, EquipoCreate, EquipoUpdate, Calibracion, CalibracionCreate, EquipoResponse
from app.services.equipment_service import equipment_service
from app.services.file_service import file_service

router = APIRouter()

@router.get("/", response_model=EquipoResponse)
def read_equipos(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 10,
    search: str = Query(None),
    estado: str = Query(None)
):
    items, total = equipment_service.get_equipos(db, skip=skip, limit=limit, search=search, estado=estado)
    return {"items": items, "total": total}

@router.post("/", response_model=Equipo)
async def create_equipo(
    *,
    db: Session = Depends(deps.get_db),
    nombre: str = Form(...),
    marca: str = Form(""),
    modelo: str = Form(""),
    numero_serie: str = Form(""),
    estado: str = Form("Activo"),
    ubicacion: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    foto_url = None
    if file:
        foto_url = await file_service.save_file(file, "equipos")
        
    equipo_in = EquipoCreate(
        nombre=nombre,
        marca=marca,
        modelo=modelo,
        numero_serie=numero_serie,
        estado=estado,
        ubicacion=ubicacion,
        foto_url=foto_url
    )
    return equipment_service.create_equipo(db=db, equipo=equipo_in)

@router.get("/{equipo_id}", response_model=Equipo)
def read_equipo(
    equipo_id: UUID,
    db: Session = Depends(deps.get_db)
):
    equipo = equipment_service.get_equipo(db, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipo

@router.put("/{equipo_id}", response_model=Equipo)
def update_equipo(
    equipo_id: UUID,
    equipo_in: EquipoUpdate,
    db: Session = Depends(deps.get_db)
):
    equipo = equipment_service.update_equipo(db, equipo_id, equipo_in)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipo

@router.delete("/{equipo_id}", response_model=dict)
def delete_equipo(
    equipo_id: UUID,
    db: Session = Depends(deps.get_db)
):
    equipo = equipment_service.delete_equipo(db, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return {"status": "success", "message": "Equipo eliminado"}

@router.post("/{equipo_id}/foto")
async def upload_photo(
    equipo_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db)
):
    equipo = equipment_service.get_equipo(db, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    
    path = await file_service.save_file(file, "equipos")
    equipment_service.update_equipo(db, equipo_id, EquipoUpdate(foto_url=path))
    return {"filename": path}

@router.get("/alerts/calibrations", response_model=List[Equipo])
def get_alerts(db: Session = Depends(deps.get_db)):
    return equipment_service.get_calibration_alerts(db)

@router.post("/calibrations", response_model=Calibracion)
async def create_calibration(
    *,
    db: Session = Depends(deps.get_db),
    equipo_id: UUID = Form(...),
    fecha_calibracion: str = Form(...),
    fecha_vencimiento: str = Form(...),
    empresa_certificadora: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    from datetime import datetime
    
    # Parse dates from string
    d_calibracion = datetime.strptime(fecha_calibracion, "%Y-%m-%d").date()
    d_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%d").date()

    certificado_url = None
    if file:
        certificado_url = await file_service.save_file(file, "certificados")
        
    calibracion_in = CalibracionCreate(
        equipo_id=equipo_id,
        fecha_calibracion=d_calibracion,
        fecha_vencimiento=d_vencimiento,
        empresa_certificadora=empresa_certificadora,
        certificado_url=certificado_url
    )
    
    return equipment_service.create_calibracion(db=db, calibracion=calibracion_in)
