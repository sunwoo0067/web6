from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data

def test_create_user_invalid_email():
    response = client.post(
        "/api/v1/users/",
        json={
            "email": "invalid-email",
            "username": "testuser",
            "password": "testpass123"
        }
    )
    assert response.status_code == 422

def test_create_duplicate_user():
    # First user
    response1 = client.post(
        "/api/v1/users/",
        json={
            "email": "duplicate@example.com",
            "username": "testuser1",
            "password": "testpass123"
        }
    )
    assert response1.status_code == 201
    
    # Duplicate user
    response2 = client.post(
        "/api/v1/users/",
        json={
            "email": "duplicate@example.com",
            "username": "testuser2",
            "password": "testpass123"
        }
    )
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Email already registered"

def test_read_users():
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_user():
    # Create a user first
    create_response = client.post(
        "/api/v1/users/",
        json={
            "email": "getuser@example.com",
            "username": "getuser",
            "password": "testpass123"
        }
    )
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "getuser@example.com"
    assert data["username"] == "getuser"

def test_read_user_not_found():
    response = client.get("/api/v1/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
