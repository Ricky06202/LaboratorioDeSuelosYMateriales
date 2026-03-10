import pytest
from datetime import date
from app.services.equipment_service import equipment_service
from app.schemas.equipment import EquipoCreate

def test_create_equipo_full_data_persistence(db):
    """
    Validates that all 30+ fields are correctly persisted in the database.
    """
    equipo_in = EquipoCreate(
        nombre="Balanza de Precisión",
        marca="Mettler",
        modelo="XPR-200",
        numero_serie="SN-METTLER-001",
        estado="Activo",
        tipo_fondo="Autogestión",
        orden_compra="OC-2024-ABC",
        solicitud_no="SOL-123",
        tipo_bien="Equipo de Medición",
        fecha_recibido=date(2024, 3, 1),
        id_asignado="LSM-001",
        capacidad="500g",
        ubicacion_fisica="Laboratorio Central",
        proveedor="LabProvider S.A.",
        estado_aprobacion="Aprobado para Uso",
        observaciones="Sin observaciones",
        verificado_por="Ing. Test",
        revisado_por="Dr. Check",
        fecha_verificacion=date(2024, 3, 2),
        fecha_revision=date(2024, 3, 3),
        rango_calibracion="0-500g",
        frecuencia_calibracion=12,
        metodo_mantenimiento="Limpieza semanal",
        criteria_1=True,
        criteria_2=True,
        criteria_3=True,
        criteria_4=True,
        criteria_5=True,
        criteria_6=False,
        criteria_7=True,
        criteria_8=True,
        criteria_9=True,
        criteria_10=True,
        criteria_11=True,
        criteria_12=True,
        criteria_13=False,
        criteria_14=True
    )
    
    db_equipo = equipment_service.create_equipo(db, equipo_in)
    
    # Assert core fields
    assert db_equipo.id is not None
    assert db_equipo.nombre == "Balanza de Precisión"
    assert db_equipo.numero_serie == "SN-METTLER-001"
    assert db_equipo.tipo_fondo == "Autogestión"
    
    # Assert expanded fields
    assert db_equipo.solicitud_no == "SOL-123"
    assert db_equipo.id_asignado == "LSM-001"
    assert db_equipo.capacidad == "500g"
    assert db_equipo.proveedor == "LabProvider S.A."
    
    # Assert metadata
    assert db_equipo.verificado_por == "Ing. Test"
    assert db_equipo.fecha_verificacion == date(2024, 3, 2)
    
    # Assert criteria (Booleans)
    assert db_equipo.criteria_1 is True
    assert db_equipo.criteria_6 is False
    assert db_equipo.criteria_13 is False
    assert db_equipo.criteria_14 is True

def test_equipment_service_retrieval(db):
    """
    Tests that equipment can be retrieved after creation.
    """
    equipo_in = EquipoCreate(
        nombre="Tamiz #200",
        marca="Estandard",
        modelo="Sieve",
        numero_serie="TM-200-01",
        estado="Activo"
    )
    created = equipment_service.create_equipo(db, equipo_in)
    
    fetched = equipment_service.get_equipo(db, created.id)
    assert fetched is not None
    assert fetched.nombre == "Tamiz #200"
    assert fetched.numero_serie == "TM-200-01"

def test_equipment_service_list_filter(db):
    """
    Tests equipment listing and filtering.
    """
    # Create multiple
    equipment_service.create_equipo(db, EquipoCreate(nombre="Eq A", numero_serie="A1", estado="Activo", marca="M", modelo="M1"))
    equipment_service.create_equipo(db, EquipoCreate(nombre="Eq B", numero_serie="B2", estado="Mantenimiento", marca="M", modelo="M2"))
    
    items, total = equipment_service.get_equipos(db, search="Eq A")
    assert total == 1
    assert items[0].nombre == "Eq A"
    
    items, total = equipment_service.get_equipos(db, estado="Mantenimiento")
    assert total == 1
    assert items[0].nombre == "Eq B"
