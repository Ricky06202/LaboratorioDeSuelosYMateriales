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

class EquipoCreate(EquipoBase):
    pass

class EquipoUpdate(BaseModel):
    nombre: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    numero_serie: Optional[str] = None
    estado: Optional[str] = None
    foto_url: Optional[str] = None

class Equipo(EquipoBase):
    id: UUID
    calibraciones: List[Calibracion] = []

    class Config:
        from_attributes = True

class EquipoResponse(BaseModel):
    items: List[Equipo]
    total: int
