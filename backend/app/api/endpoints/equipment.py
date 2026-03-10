from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, Form
from fastapi.responses import FileResponse, Response
from app.api.endpoints.pdf_utils import render_pdf
import os
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.api import deps
from app.schemas.equipment import Equipo, EquipoCreate, EquipoUpdate, Calibracion, CalibracionCreate, EquipoResponse
from app.services.equipment_service import equipment_service
from app.services.file_service import file_service

from fastapi.responses import JSONResponse
import traceback

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
    tipo_fondo: Optional[str] = Form(None),
    orden_compra: Optional[str] = Form(None),
    solicitud_no: Optional[str] = Form(None),
    tipo_bien: Optional[str] = Form(None),
    fecha_recibido: Optional[str] = Form(None),
    id_asignado: Optional[str] = Form(None),
    capacidad: Optional[str] = Form(None),
    ubicacion_fisica: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    from datetime import datetime
    d_recibido = None
    if fecha_recibido:
        d_recibido = datetime.strptime(fecha_recibido, "%Y-%m-%d").date()

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
        foto_url=foto_url,
        tipo_fondo=tipo_fondo,
        orden_compra=orden_compra,
        solicitud_no=solicitud_no,
        tipo_bien=tipo_bien,
        fecha_recibido=d_recibido,
        id_asignado=id_asignado,
        capacidad=capacidad,
        ubicacion_fisica=ubicacion_fisica
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

@router.get("/files/download/{type}/{filename}")
def download_file(
    type: str,
    filename: str,
    current_user = Depends(deps.get_current_active_user)
):
    """
    Protected endpoint to serve files. Requires a valid JWT token.
    Type should be 'equipos' or 'certificados'.
    """
    if type not in ["equipos", "certificados"]:
        raise HTTPException(status_code=400, detail="Tipo de archivo inválido")
        
    from app.core.config import settings
    full_path = os.path.join(settings.STORAGE_PATH, type, filename)
    
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
        
    return FileResponse(full_path)

@router.get("/reports/glassware", response_class=Response)
def generate_glassware_report(
    db: Session = Depends(deps.get_db),
    # If a valid JWT token is needed, we could add dependecy here, e.g.
    # current_user = Depends(deps.get_current_active_user)
):
    equipos, _ = equipment_service.get_equipos(db, skip=0, limit=1000)
    items = []
    
    for equipo in equipos:
        items.append({
            "inventory_code": equipo.numero_serie or "",
            "asset_number": "No Aplica",
            "equipment_name": equipo.nombre or "",
            "manufacturer": equipo.marca or "",
            "serial_number": equipo.numero_serie or "",
            "capacity": equipo.modelo or "",
            "location": "AREA-1",
            "maintenance_method": "N/A",
            "calibration_method": "N/A",
            "calibration_period": "N/A",
            "last_calibration": "",
            "calibrated_by": ""
        })
        
    pdf_bytes = render_pdf("glassware_inventory.html", {"items": items})
    return Response(content=pdf_bytes, media_type="application/pdf")

@router.get("/reports/calibration", response_class=Response)
def generate_calibration_report(
    db: Session = Depends(deps.get_db)
):
    equipos, _ = equipment_service.get_equipos(db, skip=0, limit=1000)
    items = []
    for equipo in equipos:
        # Get the most recent calibration if available
        # Need to safely access relationships. Assuming equipo.calibraciones is populated
        last_calib = equipo.calibraciones[-1] if (hasattr(equipo, "calibraciones") and equipo.calibraciones) else None
        
        items.append({
            "internal_inventory_number": equipo.numero_serie or "",
            "utp_asset_number": "No Aplica",
            "brand_model": f"{equipo.marca or ''} / {equipo.modelo or ''}",
            "equipment_instrument": equipo.nombre or "",
            "calibration_name": equipo.nombre or "",
            "calibration_range": "N/A",
            "calibrated_by": last_calib.empresa_certificadora if last_calib else "N/A",
            "calibration_frequency": "1 Año" if last_calib else "N/A",
            "last_calibration_date": str(last_calib.fecha_calibracion) if last_calib else "N/A",
            "next_calibration_date": str(last_calib.fecha_vencimiento) if last_calib else "N/A"
        })
        
    pdf_bytes = render_pdf("calibration_program.html", {"items": items})
    return Response(content=pdf_bytes, media_type="application/pdf")

@router.get("/reports/measurement", response_class=Response)
def generate_measurement_equipment_report(
    db: Session = Depends(deps.get_db)
):
    equipos, _ = equipment_service.get_equipos(db, skip=0, limit=1000)
    items = []
    
    for equipo in equipos:
        last_calib = equipo.calibraciones[-1] if (hasattr(equipo, "calibraciones") and equipo.calibraciones) else None

        items.append({
            "inventory_code": equipo.numero_serie or "",
            "equipment_name": equipo.nombre or "",
            "manufacturer": equipo.marca or "",
            "serial_number": equipo.numero_serie or "",
            "capacity": equipo.modelo or "",
            "location": "AREA-1",
            "maintenance_method": "N/A",
            "calibration_method": "N/A",
            "calibration_period": "1 Año" if last_calib else "N/A",
            "last_calibration": str(last_calib.fecha_calibracion) if last_calib else "",
            "calibrated_by": last_calib.empresa_certificadora if last_calib else "",
            "reference_material": "N/A",
            "damage_assessment": "No" if equipo.estado == "Activo" else "Sí"
        })
        
    pdf_bytes = render_pdf("measurement_equipment_inventory.html", {"items": items})
    return Response(content=pdf_bytes, media_type="application/pdf")

@router.get("/reports/field_aux", response_class=Response)
def generate_field_aux_equipment_report(
    db: Session = Depends(deps.get_db)
):
    equipos, _ = equipment_service.get_equipos(db, skip=0, limit=1000)
    items = []
    
    for equipo in equipos:
        items.append({
            "lab_id": equipo.numero_serie or "",
            "utp_active_number": "No Aplica",
            "equipment_name": equipo.nombre or "",
            "manufacturer_name": equipo.marca or "",
            "brand": equipo.marca or "",
            "model": equipo.modelo or "",
            "serial_number": equipo.numero_serie or "",
            "ranges": "N/A",
            "status": equipo.estado or "",
            "location": "AREA-1"
        })
        
    pdf_bytes = render_pdf("field_aux_equipment_inventory.html", {"items": items})
    return Response(content=pdf_bytes, media_type="application/pdf")

@router.get("/reports/maintenance_plan", response_class=Response)
def generate_maintenance_plan_report(
    db: Session = Depends(deps.get_db)
):
    equipos, _ = equipment_service.get_equipos(db, skip=0, limit=1000)
    items = []
    
    for equipo in equipos:
        last_calib = equipo.calibraciones[-1] if (hasattr(equipo, "calibraciones") and equipo.calibraciones) else None

        items.append({
            "equipment_id": equipo.numero_serie or "",
            "equipment_name": equipo.nombre or "",
            "criteria": "Manual del fabricante", # Default example
            "activity": "Mantenimiento / Calibración",
            "frequency": "1 Año",
            "internal_resp": "LSMCH" if not last_calib else "",
            "external_resp": last_calib.empresa_certificadora if last_calib else ""
        })
        
    pdf_bytes = render_pdf("verification_maintenance_plan.html", {"items": items})
    return Response(content=pdf_bytes, media_type="application/pdf")

@router.get("/reports/reagents", response_class=Response)
def generate_reagents_registry_report(
    db: Session = Depends(deps.get_db)
):
    equipos, _ = equipment_service.get_equipos(db, skip=0, limit=1000)
    items = []
    
    # In a real scenario, this would likely query a different model (e.g. Reactivos) 
    # instead of Equipos, but for now we map it as an example.
    for equipo in equipos:
        items.append({
            "receive_date": "N/A",
            "item_name": equipo.nombre or "",
            "purchase_ref": "N/A",
            "brand": equipo.marca or "",
            "description": equipo.modelo or "",
            "presentation": "N/A",
            "quantity": "1",
            "reagent_type": "N/A",
            "catalog_batch": equipo.numero_serie or "",
            "provider": "N/A",
            "expiry_date": "N/A",
            "assigned_id": equipo.numero_serie or "",
            "storage_area": "AREA-1",
            "container_eval": "",
            "label_eval": "",
            "cert_eval": "",
            "evaluator_tech": "",
            "observations": ""
        })
        
    pdf_bytes = render_pdf("chemical_reagents_registry.html", {"items": items})
    return Response(content=pdf_bytes, media_type="application/pdf")

@router.get("/reports/purchase_verification", response_class=Response)
def generate_purchase_verification_report(
    db: Session = Depends(deps.get_db)
):
    # In a real scenario, this would likely query a different model (e.g. Purchases/Recepciones)
    # but for now we map it with dummy data to demonstrate the PDF generation.
    data = {
        "fund_type": "Funcionamiento",
        "purchase_order_no": "OC-2025-001",
        "request_no": "REQ-2025-001",
        "item_type": "Equipo de Medición",
        "item_name": "Balanza Analítica",
        "brand": "Ohaus",
        "model": "Explorer",
        "serial": "SN-123456789",
        "provider": "Equipos de Laboratorio S.A.",
        "receive_date": "2025-10-15",
        "assigned_id": "001",
        "criteria_1": "SI", "criteria_2": "SI", "criteria_3": "SI",
        "criteria_4": "SI", "criteria_5": "SI", "criteria_6": "SI",
        "criteria_7": "SI", "criteria_8": "SI", "criteria_9": "NO",
        "criteria_10": "SI", "criteria_11": "SI", "criteria_12": "SI",
        "criteria_13": "NO", "criteria_14": "SI",
        "approval_status": "Aprobado para Uso",
        "observations": "Ninguna",
        "verified_by": "Lic. Juan Perez",
        "reviewed_by": "Lic. María Gonzalez",
        "verification_date": "2025-10-16",
        "review_date": "2025-10-17"
    }
        
    pdf_bytes = render_pdf("purchase_verification.html", {"data": data})
    return Response(content=pdf_bytes, media_type="application/pdf")

@router.get("/reports/acquisition_registry", response_class=Response)
def generate_acquisition_registry_report(
    db: Session = Depends(deps.get_db)
):
    equipos, _ = equipment_service.get_equipos(db, skip=0, limit=1000)
    items = []
    
    for equipo in equipos:
        items.append({
            "receive_date": str(equipo.fecha_adquisicion) if hasattr(equipo, 'fecha_adquisicion') and equipo.fecha_adquisicion else "N/A",
            "item_name": equipo.nombre or "",
            "utp_active_no": "N/A",
            "funds": "A", # Default: Autogestión
            "brand": equipo.marca or "",
            "description": equipo.modelo or "",
            "catalog": equipo.numero_serie or "",
            "provider": "N/A",
            "evaluated_by": "J. Quiel",
            "storage_area": "AREA-1",
            "assigned_id": equipo.numero_serie or "",
            "received_by": "LSMCH"
        })
        
    pdf_bytes = render_pdf("equipment_acquisition_registry.html", {"items": items})
    return Response(content=pdf_bytes, media_type="application/pdf")
