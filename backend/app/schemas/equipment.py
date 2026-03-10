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
    proveedor: Optional[str] = None
    estado_aprobacion: Optional[str] = None
    observaciones: Optional[str] = None
    verificado_por: Optional[str] = None
    revisado_por: Optional[str] = None
    fecha_verificacion: Optional[date] = None
    fecha_revision: Optional[date] = None
    rango_calibracion: Optional[str] = None
    frecuencia_calibracion: Optional[int] = None
    metodo_mantenimiento: Optional[str] = None
    
    # Criteria fields
    criteria_1: bool = True
    criteria_2: bool = True
    criteria_3: bool = True
    criteria_4: bool = True
    criteria_5: bool = True
    criteria_6: bool = False
    criteria_7: bool = True
    criteria_8: bool = True
    criteria_9: bool = True
    criteria_10: bool = True
    criteria_11: bool = True
    criteria_12: bool = True
    criteria_13: bool = False
    criteria_14: bool = True

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
    proveedor: Optional[str] = None
    estado_aprobacion: Optional[str] = None
    observaciones: Optional[str] = None
    verificado_por: Optional[str] = None
    revisado_por: Optional[str] = None
    fecha_verificacion: Optional[date] = None
    fecha_revision: Optional[date] = None
    rango_calibracion: Optional[str] = None
    frecuencia_calibracion: Optional[int] = None
    metodo_mantenimiento: Optional[str] = None
    
    criteria_1: Optional[bool] = None
    criteria_2: Optional[bool] = None
    criteria_3: Optional[bool] = None
    criteria_4: Optional[bool] = None
    criteria_5: Optional[bool] = None
    criteria_6: Optional[bool] = None
    criteria_7: Optional[bool] = None
    criteria_8: Optional[bool] = None
    criteria_9: Optional[bool] = None
    criteria_10: Optional[bool] = None
    criteria_11: Optional[bool] = None
    criteria_12: Optional[bool] = None
    criteria_13: Optional[bool] = None
    criteria_14: Optional[bool] = None

class Equipo(EquipoBase):
    id: UUID
    calibraciones: List[Calibracion] = []

    class Config:
        from_attributes = True

class EquipoResponse(BaseModel):
    items: List[Equipo]
    total: int
