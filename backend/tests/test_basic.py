from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_read_root():
    """Test básico para verificar que el servidor responde"""
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "ok"