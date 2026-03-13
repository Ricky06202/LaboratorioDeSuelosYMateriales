import pytest
from fastapi import status
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.customer import Customer
from app.models.lab_service import LabService
from app.core.security import get_password_hash


# ==================== QUOTATION TESTS ====================

def test_create_quotation(client, test_user, test_customer, test_lab_service):
    """Test creating a quotation"""
    # Login
    response = client.post("/api/auth/login/access-token", data={
        "username": "testuser@test.com",
        "password": "testpassword123"
    })
    token = response.json()["access_token"]
    
    # Create quotation
    response = client.post(
        "/api/cotizaciones/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "client_name": test_customer.name,
            "client_ruc": test_customer.ruc,
            "client_direction": test_customer.address,
            "client_phone": test_customer.phone,
            "client_email": test_customer.email,
            "project_name": "Test Project",
            "project_location": "Test Location",
            "items": [
                {
                    "description": test_lab_service.name,
                    "item_norma": test_lab_service.norm,
                    "item_sample": "Concreto",
                    "amount": 2,
                    "unit_price": test_lab_service.unit_price
                }
            ],
            "mobilization_cost": 50.0,
            "viatics_cost": 30.0
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["client_name"] == test_customer.name
    assert data["project_name"] == "Test Project"
    assert len(data["items"]) == 1


def test_get_quotations(client, test_user):
    """Test getting all quotations"""
    # Login
    response = client.post("/api/auth/login/access-token", data={
        "username": "testuser@test.com",
        "password": "testpassword123"
    })
    token = response.json()["access_token"]
    
    # Get quotations
    response = client.get(
        "/api/cotizaciones/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_quotation_by_id(client, test_user, test_customer, test_lab_service):
    """Test getting a specific quotation"""
    # Login
    response = client.post("/api/auth/login/access-token", data={
        "username": "testuser@test.com",
        "password": "testpassword123"
    })
    token = response.json()["access_token"]
    
    # Create quotation first
    create_response = client.post(
        "/api/cotizaciones/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "client_name": test_customer.name,
            "client_ruc": test_customer.ruc,
            "client_phone": test_customer.phone,
            "project_name": "Test Project",
            "items": [
                {
                    "description": test_lab_service.name,
                    "amount": 1,
                    "unit_price": 100.0
                }
            ]
        }
    )
    quotation_id = create_response.json()["id"]
    
    # Get quotation
    response = client.get(
        f"/api/cotizaciones/{quotation_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == quotation_id
