import os
import io
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_file():
    # First create a user
    user_response = client.post(
        "/api/v1/users/",
        json={
            "email": "fileuser@example.com",
            "username": "fileuser",
            "password": "testpass123"
        }
    )
    user_id = user_response.json()["id"]
    
    # Create a test file
    file_content = b"Hello, this is a test file!"
    files = {
        "file": ("test.txt", io.BytesIO(file_content), "text/plain")
    }
    
    # Upload file
    response = client.post(
        f"/api/v1/files/upload/{user_id}",
        files=files
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.txt"
    assert data["content_type"] == "text/plain"
    assert data["user_id"] == user_id
    
    # Verify file exists on disk
    assert os.path.exists(data["file_path"])
    with open(data["file_path"], "rb") as f:
        assert f.read() == file_content
    
    # Cleanup
    os.remove(data["file_path"])

def test_read_user_files():
    # Create a user
    user_response = client.post(
        "/api/v1/users/",
        json={
            "email": "multifileuser@example.com",
            "username": "multifileuser",
            "password": "testpass123"
        }
    )
    user_id = user_response.json()["id"]
    
    # Upload multiple files
    file_names = ["first.txt", "second.txt", "third.txt"]
    uploaded_files = []
    
    for name in file_names:
        files = {
            "file": (name, io.BytesIO(f"Content of {name}".encode()), "text/plain")
        }
        response = client.post(
            f"/api/v1/files/upload/{user_id}",
            files=files
        )
        uploaded_files.append(response.json())
    
    # Get user's files
    response = client.get(f"/api/v1/files/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert all(file["user_id"] == user_id for file in data)
    assert all(file["filename"] in file_names for file in data)
    
    # Cleanup
    for file in uploaded_files:
        os.remove(file["file_path"])

def test_delete_file():
    # Create a user
    user_response = client.post(
        "/api/v1/users/",
        json={
            "email": "deletefile@example.com",
            "username": "deletefile",
            "password": "testpass123"
        }
    )
    user_id = user_response.json()["id"]
    
    # Upload a file
    files = {
        "file": ("delete.txt", io.BytesIO(b"Delete me!"), "text/plain")
    }
    upload_response = client.post(
        f"/api/v1/files/upload/{user_id}",
        files=files
    )
    file_id = upload_response.json()["id"]
    file_path = upload_response.json()["file_path"]
    
    # Verify file exists
    assert os.path.exists(file_path)
    
    # Delete file
    response = client.delete(
        f"/api/v1/files/{file_id}",
        params={"user_id": user_id}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    
    # Verify file is deleted from disk
    assert not os.path.exists(file_path)
    
    # Verify file is deleted from database
    get_response = client.get(f"/api/v1/files/{file_id}")
    assert get_response.status_code == 404

def test_unauthorized_delete():
    # Create two users
    user1_response = client.post(
        "/api/v1/users/",
        json={
            "email": "user1file@example.com",
            "username": "user1file",
            "password": "testpass123"
        }
    )
    user1_id = user1_response.json()["id"]
    
    user2_response = client.post(
        "/api/v1/users/",
        json={
            "email": "user2file@example.com",
            "username": "user2file",
            "password": "testpass123"
        }
    )
    user2_id = user2_response.json()["id"]
    
    # User1 uploads a file
    files = {
        "file": ("user1.txt", io.BytesIO(b"User1's file"), "text/plain")
    }
    upload_response = client.post(
        f"/api/v1/files/upload/{user1_id}",
        files=files
    )
    file_id = upload_response.json()["id"]
    file_path = upload_response.json()["file_path"]
    
    # User2 tries to delete User1's file
    response = client.delete(
        f"/api/v1/files/{file_id}",
        params={"user_id": user2_id}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "File not found or not authorized"
    
    # Verify file still exists
    assert os.path.exists(file_path)
    
    # Cleanup
    os.remove(file_path)

def teardown_module(module):
    # Cleanup uploads directory after all tests
    if os.path.exists("uploads"):
        for file in os.listdir("uploads"):
            file_path = os.path.join("uploads", file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir("uploads")
