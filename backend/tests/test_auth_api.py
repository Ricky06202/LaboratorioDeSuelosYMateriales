import pytest
from fastapi import status
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.customer import Customer
from app.models.lab_service import LabService
from app.core.security import get_password_hash


# ==================== AUTH TESTS ====================

def test_login_success(client, test_user):
    """Test successful login"""
    response = client.post(
        "/api/auth/login/access-token",
        data={
            "username": "testuser@test.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user):
    """Test login with wrong password"""
    response = client.post(
        "/api/auth/login/access-token",
        data={
            "username": "testuser@test.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_nonexistent_user(client):
    """Test login with nonexistent user"""
    response = client.post(
        "/api/auth/login/access-token",
        data={
            "username": "nonexistent@test.com",
            "password": "anypassword"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_inactive_user(client, db):
    """Test login with inactive user"""
    from app.models.user import User
    from app.core.security import get_password_hash
    
    user = User(
        email="inactive@test.com",
        full_name="Inactive User",
        hashed_password=get_password_hash("password"),
        is_active=False
    )
    db.add(user)
    db.commit()
    
    response = client.post(
        "/api/auth/login/access-token",
        data={
            "username": "inactive@test.com",
            "password": "password"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
