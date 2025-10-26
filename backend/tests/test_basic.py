from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_read_root():
    """Test básico para verificar que el servidor responde"""
    response = client.get("/")
    assert response.status_code == 200

def test_health_check():
    """Test para verificar que el servidor está funcionando"""
    response = client.get("/")
    assert response.status_code == 200