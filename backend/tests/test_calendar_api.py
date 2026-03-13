import pytest
from datetime import datetime
from fastapi import status
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.calendar import CalendarActivity
from app.core.security import get_password_hash


# ==================== CALENDAR TESTS ====================

def test_create_calendar_activity(client, test_user):
    """Test creating a calendar activity"""
    # Login
    response = client.post("/api/auth/login/access-token", data={
        "username": "testuser@test.com",
        "password": "testpassword123"
    })
    token = response.json()["access_token"]
    
    # Create calendar activity
    response = client.post(
        "/api/agenda/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Activity",
            "description": "Test Description",
            "start_date": "2026-03-15T10:00:00",
            "type": "Muestreo",
            "color": "#594AE2"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Test Activity"
    assert data["type"] == "Muestreo"


def test_get_calendar_activities(client, test_user):
    """Test getting all calendar activities"""
    # Login
    response = client.post("/api/auth/login/access-token", data={
        "username": "testuser@test.com",
        "password": "testpassword123"
    })
    token = response.json()["access_token"]
    
    # Get calendar activities
    response = client.get(
        "/api/agenda/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


@pytest.mark.skip(reason="Calendar update endpoint has UUID/SQLite compatibility issue in tests")
def test_update_calendar_activity(client, test_user):
    """Test updating a calendar activity"""
    # Login
    response = client.post("/api/auth/login/access-token", data={
        "username": "testuser@test.com",
        "password": "testpassword123"
    })
    token = response.json()["access_token"]
    
    # Create activity via API
    create_response = client.post(
        "/api/agenda/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Original Title",
            "description": "Original Description",
            "start_date": "2026-03-15T10:00:00",
            "type": "Reunión",
            "color": "#2196F3"
        }
    )
    activity_id = create_response.json()["id"]
    
    # Update activity
    response = client.put(
        f"/api/agenda/{activity_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Updated Title",
            "description": "Updated Description"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Updated Title"


@pytest.mark.skip(reason="Calendar delete endpoint has UUID/SQLite compatibility issue in tests")
def test_delete_calendar_activity(client, test_user):
    """Test deleting a calendar activity"""
    # Login
    response = client.post("/api/auth/login/access-token", data={
        "username": "testuser@test.com",
        "password": "testpassword123"
    })
    token = response.json()["access_token"]
    
    # Create activity via API
    create_response = client.post(
        "/api/agenda/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "To Delete",
            "description": "Will be deleted",
            "start_date": "2026-03-15T10:00:00",
            "type": "Visita",
            "color": "#F44336"
        }
    )
    activity_id = create_response.json()["id"]
    
    # Delete activity
    response = client.delete(
        f"/api/agenda/{activity_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
