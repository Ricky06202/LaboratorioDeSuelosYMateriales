import enum
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Enum, Table, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
import uuid
from app.db.base_class import Base

class EquipoStatus(str, enum.Enum):
    Activo = "Activo"
    Danado = "Danado"
    Mantenimiento = "Mantenimiento"
    Baja = "Baja"

class Equipo(Base):
    __tablename__ = "equipos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, index=True, nullable=False)
    marca = Column(String)
    modelo = Column(String)
    numero_serie = Column(String, unique=True, index=True)
    estado = Column(Enum(EquipoStatus), default=EquipoStatus.Activo)
    foto_url = Column(String, nullable=True)
    ubicacion = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)
    fecha_proxima_calibracion = Column(Date, nullable=True)
    
    # New fields for wizard/LSMCH forms
    tipo_fondo = Column(String, nullable=True)
    orden_compra = Column(String, nullable=True)
    solicitud_no = Column(String, nullable=True)
    tipo_bien = Column(String, nullable=True)
    fecha_recibido = Column(Date, nullable=True)
    id_asignado = Column(String, nullable=True)
    capacidad = Column(String, nullable=True)
    ubicacion_fisica = Column(String, nullable=True)
    proveedor = Column(String, nullable=True)
    estado_aprobacion = Column(String, nullable=True)
    observaciones = Column(String, nullable=True)
    verificado_por = Column(String, nullable=True)
    revisado_por = Column(String, nullable=True)
    fecha_verificacion = Column(Date, nullable=True)
    fecha_revision = Column(Date, nullable=True)
    rango_calibracion = Column(String, nullable=True)
    frecuencia_calibracion = Column(Integer, nullable=True)
    metodo_mantenimiento = Column(String, nullable=True)
    
    # Verification criteria columns
    criteria_1 = Column(Boolean, default=True)
    criteria_2 = Column(Boolean, default=True)
    criteria_3 = Column(Boolean, default=True)
    criteria_4 = Column(Boolean, default=True)
    criteria_5 = Column(Boolean, default=True)
    criteria_6 = Column(Boolean, default=False)
    criteria_7 = Column(Boolean, default=True)
    criteria_8 = Column(Boolean, default=True)
    criteria_9 = Column(Boolean, default=True)
    criteria_10 = Column(Boolean, default=True)
    criteria_11 = Column(Boolean, default=True)
    criteria_12 = Column(Boolean, default=True)
    criteria_13 = Column(Boolean, default=False)
    criteria_14 = Column(Boolean, default=True)

    # Passive deletes / no cascade to enforce RESTRICT on physical deletion
    calibraciones = relationship("Calibracion", back_populates="equipo")

class Calibracion(Base):
    __tablename__ = "calibraciones"

    id = Column(Integer, primary_key=True, index=True)
    equipo_id = Column(UUID(as_uuid=True), ForeignKey("equipos.id"))
    fecha_calibracion = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    empresa_certificadora = Column(String)
    certificado_url = Column(String, nullable=True)

    equipo = relationship("Equipo", back_populates="calibraciones")
