# Documentación de la API

## Endpoints

### Autenticación

#### POST /login
- **Descripción**: Autenticación de médicos
- **Body**:
  ```json
  {
    "username": "email@ejemplo.com",
    "password": "contraseña"
  }
  ```
- **Respuesta**:
  ```json
  {
    "access_token": "token...",
    "token_type": "bearer"
  }
  ```

#### POST /registro
- **Descripción**: Registro de nuevos médicos
- **Body**:
  ```json
  {
    "nombre": "Dr. Ejemplo",
    "email": "email@ejemplo.com",
    "password": "contraseña",
    "especialidad": "Medicina General"
  }
  ```

### Gestión de Pacientes

#### GET /pacientes/
- **Descripción**: Obtener lista de pacientes
- **Requiere**: Token JWT
- **Respuesta**: Lista de pacientes

#### POST /pacientes/
- **Descripción**: Crear nuevo paciente
- **Requiere**: Token JWT
- **Body**:
  ```json
  {
    "nombre": "Paciente Ejemplo",
    "edad": 30,
    "historialMedico": "Historia médica del paciente"
  }
  ```

#### GET /pacientes/{id_paciente}
- **Descripción**: Obtener detalles de un paciente
- **Requiere**: Token JWT
- **Parámetros**: ID del paciente

#### DELETE /pacientes/{id_paciente}
- **Descripción**: Eliminar un paciente
- **Requiere**: Token JWT
- **Parámetros**: ID del paciente

## Autenticación

La API utiliza autenticación JWT (JSON Web Tokens). Para acceder a los endpoints protegidos:
1. Obtener token mediante /login
2. Incluir el token en el header: `Authorization: Bearer <token>`

## Errores Comunes

- 401: No autorizado - Token inválido o expirado
- 404: No encontrado - Recurso no existe
- 400: Solicitud incorrecta - Datos inválidos
- 500: Error interno del servidor

## Ejemplo de Uso

```python
import requests

# Login
response = requests.post('http://localhost:8000/login', 
    data={'username': 'doctor@ejemplo.com', 'password': '123456'})
token = response.json()['access_token']

# Crear paciente
headers = {'Authorization': f'Bearer {token}'}
response = requests.post('http://localhost:8000/pacientes/', 
    json={
        'nombre': 'Juan Pérez',
        'edad': 35,
        'historialMedico': 'Paciente sano'
    },
    headers=headers
)
```