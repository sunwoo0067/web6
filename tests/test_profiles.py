from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_profile():
    # First create a user
    user_response = client.post(
        "/api/v1/users/",
        json={
            "email": "profile@example.com",
            "username": "profileuser",
            "password": "testpass123"
        }
    )
    user_id = user_response.json()["id"]
    
    # Create profile
    response = client.post(
        f"/api/v1/profiles/{user_id}",
        json={
            "full_name": "Test User",
            "bio": "This is a test bio",
            "avatar_url": "https://example.com/avatar.jpg"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Test User"
    assert data["bio"] == "This is a test bio"
    assert data["user_id"] == user_id

def test_read_profile():
    # Create a user and profile first
    user_response = client.post(
        "/api/v1/users/",
        json={
            "email": "readprofile@example.com",
            "username": "readprofile",
            "password": "testpass123"
        }
    )
    user_id = user_response.json()["id"]
    
    client.post(
        f"/api/v1/profiles/{user_id}",
        json={
            "full_name": "Read Test User",
            "bio": "Read test bio",
            "avatar_url": "https://example.com/avatar.jpg"
        }
    )
    
    response = client.get(f"/api/v1/profiles/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Read Test User"
    assert data["bio"] == "Read test bio"

def test_update_profile():
    # Create a user and profile first
    user_response = client.post(
        "/api/v1/users/",
        json={
            "email": "updateprofile@example.com",
            "username": "updateprofile",
            "password": "testpass123"
        }
    )
    user_id = user_response.json()["id"]
    
    client.post(
        f"/api/v1/profiles/{user_id}",
        json={
            "full_name": "Update Test User",
            "bio": "Update test bio",
            "avatar_url": "https://example.com/avatar.jpg"
        }
    )
    
    response = client.put(
        f"/api/v1/profiles/{user_id}",
        json={
            "full_name": "Updated Name",
            "bio": "Updated bio"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"
    assert data["bio"] == "Updated bio"

def test_delete_profile():
    # Create a user and profile first
    user_response = client.post(
        "/api/v1/users/",
        json={
            "email": "deleteprofile@example.com",
            "username": "deleteprofile",
            "password": "testpass123"
        }
    )
    user_id = user_response.json()["id"]
    
    client.post(
        f"/api/v1/profiles/{user_id}",
        json={
            "full_name": "Delete Test User",
            "bio": "Delete test bio",
            "avatar_url": "https://example.com/avatar.jpg"
        }
    )
    
    response = client.delete(f"/api/v1/profiles/{user_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    
    # Verify profile is deleted
    get_response = client.get(f"/api/v1/profiles/{user_id}")
    assert get_response.status_code == 404
