import pytest
from fastapi import status
from sqlalchemy.orm import Session
from app.models.user import User, Role
from app.models.customer import Customer
from app.models.lab_service import LabService
from app.core.security import get_password_hash


# ==================== USER TESTS ====================

def test_get_current_user_info(client, test_user):
    """Test getting current user info"""
    # First login to get token
    response = client.post("/api/auth/login/access-token", data={
        "username": "testuser@test.com",
        "password": "testpassword123"
    })
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]
    
    # Get current user
    response = client.get(
        "/api/usuarios/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "testuser@test.com"
    assert data["full_name"] == "Test User"


def test_update_current_user_profile(client, test_user):
    """Test updating user profile"""
    # First login
    response = client.post("/api/auth/login/access-token", data={
        "username": "testuser@test.com",
        "password": "testpassword123"
    })
    token = response.json()["access_token"]
    
    # Update profile
    response = client.put(
        "/api/usuarios/me",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "full_name": "Updated Name",
            "phone": "98765432",
            "cell_phone": "12345678",
            "cedula": "8-999-999"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["full_name"] == "Updated Name"
    assert data["phone"] == "98765432"


def test_change_password_success(client, test_user):
    """Test changing password successfully"""
    # First login
    response = client.post("/api/auth/login/access-token", data={
        "username": "testuser@test.com",
        "password": "testpassword123"
    })
    token = response.json()["access_token"]
    
    # Change password
    response = client.post(
        "/api/usuarios/me/password",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "current_password": "testpassword123",
            "new_password": "newpassword456",
            "confirm_password": "newpassword456"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    
    # Verify new password works
    response = client.post("/api/auth/login/access-token", data={
        "username": "testuser@test.com",
        "password": "newpassword456"
    })
    assert response.status_code == status.HTTP_200_OK


def test_change_password_wrong_current(client, test_user):
    """Test changing password with wrong current password"""
    # First login
    response = client.post("/api/auth/login/access-token", data={
        "username": "testuser@test.com",
        "password": "testpassword123"
    })
    token = response.json()["access_token"]
    
    # Try to change password with wrong current password
    response = client.post(
        "/api/usuarios/me/password",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "current_password": "wrongpassword",
            "new_password": "newpassword456",
            "confirm_password": "newpassword456"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_change_password_mismatch(client, test_user):
    """Test changing password with mismatched confirmation"""
    # First login
    response = client.post("/api/auth/login/access-token", data={
        "username": "testuser@test.com",
        "password": "testpassword123"
    })
    token = response.json()["access_token"]
    
    # Try to change password with mismatched confirmation
    response = client.post(
        "/api/usuarios/me/password",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "current_password": "testpassword123",
            "new_password": "newpassword456",
            "confirm_password": "differentpassword"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_all_users_as_admin(client, admin_user):
    """Test getting all users as admin"""
    # Login as admin
    response = client.post("/api/auth/login/access-token", data={
        "username": "admin@test.com",
        "password": "adminpass123"
    })
    token = response.json()["access_token"]
    
    # Get all users
    response = client.get(
        "/api/usuarios/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    users = response.json()
    assert isinstance(users, list)


def test_get_all_users_as_non_admin_forbidden(client, test_user):
    """Test that non-admin cannot get all users"""
    # Login as regular user
    response = client.post("/api/auth/login/access-token", data={
        "username": "testuser@test.com",
        "password": "testpassword123"
    })
    token = response.json()["access_token"]
    
    # Try to get all users
    response = client.get(
        "/api/usuarios/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_user_as_admin(client, admin_user):
    """Test creating a new user as admin"""
    # Login as admin
    response = client.post("/api/auth/login/access-token", data={
        "username": "admin@test.com",
        "password": "adminpass123"
    })
    token = response.json()["access_token"]
    
    # Create new user
    response = client.post(
        "/api/usuarios/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "email": "newuser@test.com",
            "password": "newuser123",
            "full_name": "New User",
            "role_ids": []
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "newuser@test.com"
    assert data["full_name"] == "New User"


def test_delete_user_as_admin(client, admin_user, db):
    """Test deleting a user as admin"""
    # Create a user to delete
    user_to_delete = User(
        email="delete@test.com",
        full_name="Delete Me",
        hashed_password=get_password_hash("password")
    )
    db.add(user_to_delete)
    db.commit()
    
    # Login as admin
    response = client.post("/api/auth/login/access-token", data={
        "username": "admin@test.com",
        "password": "adminpass123"
    })
    token = response.json()["access_token"]
    
    # Delete user
    response = client.delete(
        f"/api/usuarios/{user_to_delete.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
