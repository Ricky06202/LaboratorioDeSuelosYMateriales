from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from uuid import UUID

class CalibracionBase(BaseModel):
    fecha_calibracion: date
    fecha_vencimiento: date
    empresa_certificadora: str
    certificado_url: Optional[str] = None

class CalibracionCreate(CalibracionBase):
    equipo_id: UUID

class Calibracion(CalibracionBase):
    id: int
    equipo_id: UUID

    class Config:
        from_attributes = True

class EquipoBase(BaseModel):
    nombre: str
    marca: str
    modelo: str
    numero_serie: str
    estado: str
    foto_url: Optional[str] = None
    ubicacion: Optional[str] = None  # WKT Format (e.g., 'POINT(lon lat)')
    fecha_proxima_calibracion: Optional[date] = None
    
    # New fields for wizard/LSMCH forms
    tipo_fondo: Optional[str] = None
    orden_compra: Optional[str] = None
    solicitud_no: Optional[str] = None
    tipo_bien: Optional[str] = None
    fecha_recibido: Optional[date] = None
    id_asignado: Optional[str] = None
    capacidad: Optional[str] = None
    ubicacion_fisica: Optional[str] = None

class EquipoCreate(EquipoBase):
    pass

class EquipoUpdate(BaseModel):
    nombre: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    numero_serie: Optional[str] = None
    estado: Optional[str] = None
    foto_url: Optional[str] = None
    ubicacion: Optional[str] = None
    fecha_proxima_calibracion: Optional[date] = None
    
    # New fields for wizard/LSMCH forms
    tipo_fondo: Optional[str] = None
    orden_compra: Optional[str] = None
    solicitud_no: Optional[str] = None
    tipo_bien: Optional[str] = None
    fecha_recibido: Optional[date] = None
    id_asignado: Optional[str] = None
    capacidad: Optional[str] = None
    ubicacion_fisica: Optional[str] = None

class Equipo(EquipoBase):
    id: UUID
    calibraciones: List[Calibracion] = []

    class Config:
        from_attributes = True

class EquipoResponse(BaseModel):
    items: List[Equipo]
    total: int
