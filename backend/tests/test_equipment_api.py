from fastapi.testclient import TestClient
import pytest

def test_create_equipo_api_basic(client: TestClient):
    """
    Validates basic equipment creation through the API.
    """
    payload = {
        "nombre": "Balanza de Campo API",
        "marca": "Ohaus",
        "modelo": "Valor 4000",
        "numero_serie": "OH-API-101",
        "estado": "Activo",
        "tipo_fondo": "Gubernamental"
    }
    
    response = client.post("/api/equipos/", data=payload)
    
    assert response.status_code == 200
    content = response.json()
    assert content["nombre"] == "Balanza de Campo API"
    assert content["numero_serie"] == "OH-API-101"

def test_create_equipo_api_with_expanded_fields(client: TestClient):
    """
    Validates API handles expanded fields and boolean criteria correctly.
    """
    payload = {
        "nombre": "Eq Expanded API",
        "numero_serie": "EXP-API-001",
        "tipo_bien": "Equipo de Medición",
        "criteria_1": "true",
        "criteria_6": "false",
        "proveedor": "Provider API",
        "ubicacion_fisica": "Area API"
    }
    
    response = client.post("/api/equipos/", data=payload)
    
    assert response.status_code == 200
    content = response.json()
    assert content["criteria_1"] is True
    assert content["criteria_6"] is False
    assert content["proveedor"] == "Provider API"

def test_equipment_pdf_report_availability(client: TestClient):
    """
    Verifies that all 6 equipment-specific PDF reports are accessible via API.
    """
    # Create target equipment
    resp = client.post("/api/equipos/", data={"nombre": "Report Test", "numero_serie": "SERIE-PDF-01", "marca": "Test", "modelo": "Test"})
    equipo_id = resp.json()["id"]
    
    reports = [
        "purchase_verification",
        "acquisition",
        "measurement",
        "field_aux",
        "glassware",
        "maintenance_plan"
    ]
    
    for r_type in reports:
        response = client.get(f"/api/equipos/{equipo_id}/reports/{r_type}")
        # Note: If report generation fails due to missing system deps (like weasyprint), 
        # this might return 500, but we want to know that the ROUTE exists.
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"

def test_get_invalid_equipment_404(client: TestClient):
    """
    Verifies 404 for non-existent equipment.
    """
    # Random UUID
    response = client.get("/api/equipos/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
