from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post(
        '/api/v1/users/',
        json={
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123'
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data['email'] == 'test@example.com'
    assert data['username'] == 'testuser'

def test_read_users():
    response = client.get('/api/v1/users/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
