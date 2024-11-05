from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login():
    # First create a user
    client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123"
        }
    )
    
    # Try to login
    response = client.post(
        "/api/v1/token",
        data={
            "username": "test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_refresh_token():
    # First login to get tokens
    client.post(
        "/api/v1/users/",
        json={
            "email": "refresh@example.com",
            "username": "refreshuser",
            "password": "testpass123"
        }
    )
    
    login_response = client.post(
        "/api/v1/token",
        data={
            "username": "refresh@example.com",
            "password": "testpass123"
        }
    )
    refresh_token = login_response.json()["refresh_token"]
    
    # Try to refresh token
    response = client.post(
        "/api/v1/refresh",
        json={"refresh_token": refresh_token}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_login_incorrect_password():
    response = client.post(
        "/api/v1/token",
        data={
            "username": "test@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401

def test_refresh_token_invalid():
    response = client.post(
        "/api/v1/refresh",
        json={"refresh_token": "invalid_token"}
    )
    assert response.status_code == 401
