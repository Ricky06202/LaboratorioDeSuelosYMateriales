import pytest
from fastapi import status
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.customer import Customer
from app.models.lab_service import LabService
from app.core.security import get_password_hash


# ==================== CUSTOMER ORDER TESTS ====================

def test_create_customer_order(client, test_user, test_customer):
    """Test creating a customer order"""
    # Login
    response = client.post("/api/auth/login/access-token", data={
        "username": "testuser@test.com",
        "password": "testpassword123"
    })
    token = response.json()["access_token"]
    
    # Create customer order
    response = client.post(
        "/api/pedidos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "client_name": test_customer.name,
            "client_ruc": test_customer.ruc,
            "client_direction": test_customer.address,
            "client_phone": test_customer.phone,
            "project_name": "Test Project",
            "project_location": "Test Location",
            "project_responsable": "John Doe",
            "project_responsable_phone": "12345678",
            "project_responsable_email": "john@test.com",
            "observations": "Test observations"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["client_name"] == test_customer.name
    assert data["project_name"] == "Test Project"


def test_get_customer_orders(client, test_user):
    """Test getting all customer orders"""
    # Login
    response = client.post("/api/auth/login/access-token", data={
        "username": "testuser@test.com",
        "password": "testpassword123"
    })
    token = response.json()["access_token"]
    
    # Get customer orders
    response = client.get(
        "/api/pedidos/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_customer_order_by_id(client, test_user, test_customer):
    """Test getting a specific customer order"""
    # Login
    response = client.post("/api/auth/login/access-token", data={
        "username": "testuser@test.com",
        "password": "testpassword123"
    })
    token = response.json()["access_token"]
    
    # Create customer order first
    create_response = client.post(
        "/api/pedidos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "client_name": test_customer.name,
            "client_ruc": test_customer.ruc,
            "client_phone": test_customer.phone,
            "project_name": "Test Project"
        }
    )
    order_id = create_response.json()["id"]
    
    # Get customer order
    response = client.get(
        f"/api/pedidos/{order_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == order_id
