import pytest
from fastapi.testclient import TestClient
from app import app
import os

@pytest.fixture
def cliente():
    return TestClient(app)

@pytest.fixture
def token_medico(cliente):
    # Primero registramos un médico de prueba
    medico_datos = {
        "nombre": "Dr. Prueba",
        "email": "doctor@test.com",
        "password": "test123",
        "especialidad": "Medicina General"
    }
    cliente.post("/registro", json=medico_datos)
    
    # Luego hacemos login para obtener el token
    response = cliente.post("/login", data={
        "username": medico_datos["email"],
        "password": medico_datos["password"]
    })
    
    return response.json()["access_token"]

def test_pagina_inicio(cliente):
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200
    assert "text/html" in respuesta.headers["content-type"]

def test_registro_medico(cliente):
    medico_datos = {
        "nombre": "Dr. Test",
        "email": "test@example.com",
        "password": "password123",
        "especialidad": "Cardiología"
    }
    respuesta = cliente.post("/registro", json=medico_datos)
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["nombre"] == medico_datos["nombre"]
    assert datos["email"] == medico_datos["email"]
    assert datos["especialidad"] == medico_datos["especialidad"]
    assert "id" in datos

def test_login_medico(cliente, token_medico):
    respuesta = cliente.post("/login", data={
        "username": "doctor@test.com",
        "password": "test123"
    })
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "access_token" in datos
    assert datos["token_type"] == "bearer"

def test_crear_paciente(cliente, token_medico):
    paciente_datos = {
        "nombre": "Juan Prueba",
        "edad": 30,
        "historialMedico": "Historial de prueba"
    }
    respuesta = cliente.post(
        "/pacientes/",
        json=paciente_datos,
        headers={"Authorization": f"Bearer {token_medico}"}
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["nombre"] == paciente_datos["nombre"]
    assert datos["edad"] == paciente_datos["edad"]
    assert datos["historialMedico"] == paciente_datos["historialMedico"]
    assert "id" in datos
    return datos["id"]

def test_obtener_pacientes(cliente, token_medico):
    respuesta = cliente.get(
        "/pacientes/",
        headers={"Authorization": f"Bearer {token_medico}"}
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert isinstance(datos, list)
    if len(datos) > 0:
        paciente = datos[0]
        assert "id" in paciente
        assert "nombre" in paciente
        assert "edad" in paciente
        assert "historialMedico" in paciente

def test_obtener_paciente(cliente, token_medico):
    # Primero creamos un paciente
    id_paciente = test_crear_paciente(cliente, token_medico)
    
    # Luego intentamos obtenerlo
    respuesta = cliente.get(
        f"/pacientes/{id_paciente}",
        headers={"Authorization": f"Bearer {token_medico}"}
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["id"] == id_paciente

def test_eliminar_paciente(cliente, token_medico):
    # Primero creamos un paciente
    id_paciente = test_crear_paciente(cliente, token_medico)
    
    # Luego lo eliminamos
    respuesta = cliente.delete(
        f"/pacientes/{id_paciente}",
        headers={"Authorization": f"Bearer {token_medico}"}
    )
    assert respuesta.status_code == 200
    
    # Verificamos que ya no existe
    respuesta = cliente.get(
        f"/pacientes/{id_paciente}",
        headers={"Authorization": f"Bearer {token_medico}"}
    )
    assert respuesta.status_code == 404

def test_acceso_no_autorizado(cliente):
    # Intentar acceder sin token
    respuesta = cliente.get("/pacientes/")
    assert respuesta.status_code == 401
    
    # Intentar crear paciente sin token
    paciente_datos = {
        "nombre": "Test",
        "edad": 30,
        "historialMedico": "Test"
    }
    respuesta = cliente.post("/pacientes/", json=paciente_datos)
    assert respuesta.status_code == 401