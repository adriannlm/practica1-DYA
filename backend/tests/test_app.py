import pytest
from fastapi.testclient import TestClient
from app import app
import jwt
from datetime import datetime, timedelta

client = TestClient(app)

# Datos de prueba
test_medico = {
    "nombre": "Dr Test",
    "email": "test@example.com",
    "password": "test1234",
    "especialidad": "Medicina General"
}

test_paciente = {
    "nombre": "Paciente Test",
    "edad": 30,
    "historialMedico": "Historia médica de prueba"
}

def create_test_token(email: str = "test@example.com"):
    """Crear un token JWT de prueba"""
    expire = datetime.utcnow() + timedelta(minutes=30)
    data = {"sub": email, "exp": expire}
    token = jwt.encode(data, "tu_clave_secreta_muy_segura", algorithm="HS256")
    return token

def test_read_root():
    """Probar la ruta raíz"""
    response = client.get("/")
    assert response.status_code == 200

def test_registro_medico():
    """Probar el registro de médicos"""
    response = client.post("/registro", json=test_medico)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_medico["email"]
    assert "password" not in data

def test_login_medico():
    """Probar el login de médicos"""
    # Primero registramos un médico
    client.post("/registro", json=test_medico)
    
    # Intentamos hacer login
    response = client.post("/login", data={
        "username": test_medico["email"],
        "password": test_medico["password"]
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_crear_paciente():
    """Probar la creación de pacientes"""
    token = create_test_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post(
        "/pacientes/",
        json=test_paciente,
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == test_paciente["nombre"]
    assert data["edad"] == test_paciente["edad"]

def test_obtener_pacientes():
    """Probar la obtención de la lista de pacientes"""
    token = create_test_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/pacientes/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_obtener_paciente_individual():
    """Probar la obtención de un paciente específico"""
    token = create_test_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Primero creamos un paciente
    response = client.post(
        "/pacientes/",
        json=test_paciente,
        headers=headers
    )
    paciente_id = response.json()["id"]
    
    # Luego intentamos obtenerlo
    response = client.get(f"/pacientes/{paciente_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == paciente_id
    assert data["nombre"] == test_paciente["nombre"]

def test_eliminar_paciente():
    """Probar la eliminación de pacientes"""
    token = create_test_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Primero creamos un paciente
    response = client.post(
        "/pacientes/",
        json=test_paciente,
        headers=headers
    )
    paciente_id = response.json()["id"]
    
    # Luego intentamos eliminarlo
    response = client.delete(f"/pacientes/{paciente_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["mensaje"] == "Paciente eliminado correctamente"

def test_acceso_no_autorizado():
    """Probar el acceso sin autenticación"""
    response = client.get("/pacientes/")
    assert response.status_code == 401

def test_registro_email_duplicado():
    """Probar el registro con email duplicado"""
    # Primer registro
    client.post("/registro", json=test_medico)
    
    # Intentar registrar el mismo email
    response = client.post("/registro", json=test_medico)
    assert response.status_code == 400
    assert "email ya está registrado" in response.json()["detail"].lower()