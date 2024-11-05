from fastapi.testclient import TestClient
import pytest
from app.main import app

client = TestClient(app)

def test_create_and_read_user():
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    created_user = response.json()
    assert created_user["email"] == user_data["email"]
    assert created_user["username"] == user_data["username"]
    assert "id" in created_user
    user_id = created_user["id"]

    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id

def test_create_duplicate_user():
    user_data = {
        "email": "duplicate@example.com",
        "username": "duplicate_user",
        "password": "testpass123"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201

    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_create_invalid_email():
    user_data = {
        "email": "invalid-email",
        "username": "testuser",
        "password": "testpass123"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 422

def test_create_and_login():
    user_data = {
        "email": "login@example.com",
        "username": "loginuser",
        "password": "testpass123"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201

    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

def test_create_and_update_profile():
    user_data = {
        "email": "profile@example.com",
        "username": "profileuser",
        "password": "testpass123"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    user_id = response.json()["id"]

    profile_data = {
        "full_name": "Test User",
        "bio": "This is a test bio",
        "avatar_url": "https://example.com/avatar.jpg"
    }
    response = client.post(f"/api/v1/profiles/{user_id}", json=profile_data)
    assert response.status_code == 200
    assert response.json()["full_name"] == profile_data["full_name"]
    assert response.json()["bio"] == profile_data["bio"]

def test_create_and_upload_file():
    # 1. Create user
    user_data = {
        "email": "file@example.com",
        "username": "fileuser",
        "password": "testpass123"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    user_id = response.json()["id"]

    # 2. Login to get token
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Upload file
    file_content = b"Hello, this is a test file!"
    files = {
        "file": ("test.txt", file_content, "text/plain")
    }
    response = client.post("/api/v1/files/upload", files=files, headers=headers)
    assert response.status_code == 201
    assert response.json()["filename"] == "test.txt"
    assert response.json()["content_type"] == "text/plain"

def test_health_check():
    response = client.get("/health-check")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_profile_crud_operations():
    # 1. Create user
    user_data = {
        "email": "profile_test@example.com",
        "username": "profile_user",
        "password": "testpass123"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    user_id = response.json()["id"]

    # 2. Create profile
    profile_data = {
        "full_name": "Test User",
        "bio": "Test bio",
        "avatar_url": "http://example.com/avatar.jpg"
    }
    response = client.post(f"/api/v1/profiles/{user_id}", json=profile_data)
    assert response.status_code == 200
    assert response.json()["full_name"] == profile_data["full_name"]
    assert response.json()["bio"] == profile_data["bio"]
    assert response.json()["avatar_url"] == profile_data["avatar_url"]

    # 3. Update profile
    updated_profile_data = {
        "full_name": "Updated Name",
        "bio": "Updated bio"
    }
    response = client.put(f"/api/v1/profiles/{user_id}", json=updated_profile_data)
    assert response.status_code == 200
    assert response.json()["full_name"] == updated_profile_data["full_name"]
    assert response.json()["bio"] == updated_profile_data["bio"]

    # 4. Delete profile
    response = client.delete(f"/api/v1/profiles/{user_id}")
    assert response.status_code == 200

    # 5. Verify profile is deleted
    response = client.get(f"/api/v1/profiles/{user_id}")
    assert response.status_code == 404

def test_file_operations():
    # 1. Create user and get token
    user_data = {
        "email": "file_test@example.com",
        "username": "file_user",
        "password": "testpass123"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    user_id = response.json()["id"]

    # Login to get token
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Upload file
    file_content = b"Hello, this is a test file content!"
    files = {
        "file": ("test_file.txt", file_content, "text/plain")
    }
    response = client.post("/api/v1/files/upload", files=files, headers=headers)
    assert response.status_code == 201
    file_id = response.json()["id"]
    assert response.json()["filename"] == "test_file.txt"
    assert response.json()["content_type"] == "text/plain"

    # 3. Get file info
    response = client.get(f"/api/v1/files/{file_id}")
    assert response.status_code == 200
    assert response.json()["filename"] == "test_file.txt"

    # 4. Download file
    response = client.get(f"/api/v1/files/download/{file_id}")
    assert response.status_code == 200
    assert response.content == file_content

    # 5. List user files
    response = client.get("/api/v1/files/my-files", headers=headers)
    assert response.status_code == 200
    files = response.json()
    assert len(files) > 0
    assert any(file["id"] == file_id for file in files)

    # 6. Delete file
    response = client.delete(f"/api/v1/files/{file_id}", headers=headers)
    assert response.status_code == 200

    # 7. Verify file is deleted
    response = client.get(f"/api/v1/files/{file_id}")
    assert response.status_code == 404
