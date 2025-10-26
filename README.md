# Tech4Health Patient Management System

Este proyecto implementa un sistema de gestión de pacientes para clínicas médicas, desarrollado como parte de la práctica de Automatización y Despliegue.

## Funcionalidades

- Registro de pacientes (nombre, edad, historial médico)
- Consulta de pacientes por ID
- Eliminación de pacientes

## Requisitos

- Python 3.9+
- FastAPI
- Docker (para despliegue)
- Git

## Instalación y Ejecución

1. Clonar el repositorio:
```bash
git clone <URL_DEL_REPOSITORIO>
cd practica1
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación:
```bash
uvicorn app.main:app --reload --port 5006
```

La API estará disponible en `http://localhost:5006`

### Ejecución con Docker

1. Construir la imagen:
```bash
docker build -t tech4health-api .
```

2. Ejecutar el contenedor:
```bash
docker run -p 5006:5006 tech4health-api
```

## Pruebas

Para ejecutar las pruebas:

```bash
pytest tests/
```

## Git Hooks

El proyecto incluye los siguientes hooks:

### Pre-commit
- Verifica el formato del código con black
- Ejecuta el linter flake8
- Ejecuta las pruebas unitarias

### Post-commit
- Genera un registro en `commit_log.txt` con información del commit

### Pre-push
- Ejecuta todas las pruebas
- Aborta el push si alguna prueba falla

### Post-push
- Muestra un mensaje de confirmación
- Recuerda verificar el pipeline de CI/CD

## CI/CD con GitHub Actions

El pipeline de CI/CD incluye:

1. Ejecución de pruebas
2. Construcción de la imagen Docker
3. Despliegue en contenedor

El workflow se ejecuta automáticamente en cada push al repositorio.

## Estructura del Proyecto

```
practica1/
├── app/
│   └── main.py
├── tests/
│   └── test_main.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── hooks/
├── Dockerfile
├── requirements.txt
└── README.md
```

## API Endpoints

- POST `/patients/` - Crear nuevo paciente
- GET `/patients/{id}` - Obtener paciente por ID
- DELETE `/patients/{id}` - Eliminar paciente
- GET `/patients/` - Listar todos los pacientes

## Documentación API

La documentación interactiva está disponible en:
- Swagger UI: `http://localhost:5006/docs`
- ReDoc: `http://localhost:5006/redoc`