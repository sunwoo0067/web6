from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
<<<<<<< HEAD
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_health_check():
    response = client.get("/health-check")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
=======
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Welcome to FastAPI'}

def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}
>>>>>>> be5220edfd9c10ca47d60657c71d9ee5d1c8aeee
