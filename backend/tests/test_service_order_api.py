import pytest
from fastapi import status
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.customer import Customer
from app.core.security import get_password_hash


# ==================== SERVICE ORDER TESTS ====================

def test_create_service_order(client, test_user, test_customer):
    """Test creating a service order"""
    # Login
    response = client.post("/api/auth/login/access-token", data={
        "username": "testuser@test.com",
        "password": "testpassword123"
    })
    token = response.json()["access_token"]
    
    # Create service order
    response = client.post(
        "/api/ordenes-servicio/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "client_name": test_customer.name,
            "client_ruc": test_customer.ruc,
            "client_dv": test_customer.dv,
            "client_direction": test_customer.address,
            "client_phone": test_customer.phone,
            "client_email": test_customer.email,
            "project_name": "Test Project",
            "project_location": "Test Location",
            "quotation_ref": "COT-001",
            "total_cost": 500.0,
            "attended_by": "Test Attendant",
            "applicant_name": "John Doe"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["client_name"] == test_customer.name
    assert data["project_name"] == "Test Project"
    assert data["total_cost"] == 500.0


def test_get_service_orders(client, test_user):
    """Test getting all service orders"""
    # Login
    response = client.post("/api/auth/login/access-token", data={
        "username": "testuser@test.com",
        "password": "testpassword123"
    })
    token = response.json()["access_token"]
    
    # Get service orders
    response = client.get(
        "/api/ordenes-servicio/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_service_order_by_id(client, test_user, test_customer):
    """Test getting a specific service order"""
    # Login
    response = client.post("/api/auth/login/access-token", data={
        "username": "testuser@test.com",
        "password": "testpassword123"
    })
    token = response.json()["access_token"]
    
    # Create service order first
    create_response = client.post(
        "/api/ordenes-servicio/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "client_name": test_customer.name,
            "client_ruc": test_customer.ruc,
            "project_name": "Test Project"
        }
    )
    order_id = create_response.json()["id"]
    
    # Get service order
    response = client.get(
        f"/api/ordenes-servicio/{order_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == order_id


def test_delete_service_order(client, test_user, test_customer):
    """Test deleting a service order"""
    # Login
    response = client.post("/api/auth/login/access-token", data={
        "username": "testuser@test.com",
        "password": "testpassword123"
    })
    token = response.json()["access_token"]
    
    # Create service order first
    create_response = client.post(
        "/api/ordenes-servicio/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "client_name": test_customer.name,
            "client_ruc": test_customer.ruc,
            "project_name": "Test Project"
        }
    )
    order_id = create_response.json()["id"]
    
    # Delete service order
    response = client.delete(
        f"/api/ordenes-servicio/{order_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
