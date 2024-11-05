from typing import Dict
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_create_user(client: TestClient):
    data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    response = client.post("/api/v1/users/", json=data)
    assert response.status_code == 200
    assert response.json()["email"] == data["email"]
    assert response.json()["full_name"] == data["full_name"]
    assert "id" in response.json()

def test_create_duplicate_user(client: TestClient, test_user: Dict[str, str]):
    data = {
        "email": test_user["email"],
        "password": "testpassword123",
        "full_name": "Another User"
    }
    response = client.post("/api/v1/users/", json=data)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]
