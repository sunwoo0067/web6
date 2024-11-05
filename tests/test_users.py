from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_db
import pytest

# Test database URL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/fastapi_test_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_user():
    response = client.post(
<<<<<<< HEAD
        "/api/v1/users/",
=======
<<<<<<< HEAD
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
=======
        '/api/v1/users/',
>>>>>>> b2ce390b7110b42e0cbce41d29456a94019515dc
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data

def test_create_duplicate_user():
    # First user
    client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123"
        }
    )
    
    # Duplicate user
    response = client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "username": "testuser2",
            "password": "testpass123"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_read_users():
    # Create a user first
    client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123"
        }
    )
    
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
<<<<<<< HEAD
    data = response.json()
    assert len(data) > 0
    assert data[0]["email"] == "test@example.com"

def test_read_user():
    # Create a user first
    create_response = client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123"
        }
    )
    user_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"

def test_read_user_not_found():
    response = client.get("/api/v1/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
=======
    assert isinstance(response.json(), list)
>>>>>>> be5220edfd9c10ca47d60657c71d9ee5d1c8aeee
>>>>>>> b2ce390b7110b42e0cbce41d29456a94019515dc
