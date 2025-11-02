
# Práctica 1 - Git Hooks y CI/CD

*Asignatura:* Despliegue y Automatización  

*Alumno:* Adrián López Martín y Alejandro Rodríguez Salán  

*Fecha:* 2 de noviembre de 2025  

---

Este proyecto fue desarrollado para la empresa ficticia *Tech4Health*, que necesita un módulo de gestión de pacientes para clínicas médicas que desean digitalizar procesos básicos.  

La aplicación es un *microservicio REST* implementado con **FastAPI** que permite:  
- Registrar pacientes (nombre, edad e historial médico).  
- Consultar pacientes por su ID.  
- Eliminar pacientes del sistema.  

Además, el proyecto incorpora automatización de pruebas, control de calidad mediante hooks de Git, e integración continua con **GitHub Actions**.

---

## Especificaciones

- *Lenguaje:* Python con FastAPI  
- *Base de datos:* En memoria (diccionario en Python)  
- *Framework de tests:* pytest  
- *Automatización:* Git Hooks locales para control de calidad  
- *CI/CD:* Workflow con GitHub Actions (test, build y despliegue con Docker)

---

## Cómo ejecutar la aplicación

### Prerrequisitos
- Python 3.10 o superior  
- pip (gestor de paquetes de Python)  
- Docker y Docker Compose (para el despliegue con contenedor)

### Ejecución local

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt


2. Ejecutar la aplicación:

   ```bash
   uvicorn app:app --reload
   ```

3. Acceder desde el navegador a:

   ```
   http://127.0.0.1:8000/docs
   ```

   (Incluye la documentación interactiva Swagger generada automáticamente por FastAPI)

---

## Ejecución con Docker

1. Construir y levantar los servicios:

   ```bash
   docker-compose up --build
   ```

2. Verificar que el contenedor está corriendo:

   ```bash
   docker ps
   ```

3. Acceder a la API desde:

   ```
   http://localhost:8000
   ```

---

## Estructura del proyecto

```
Practica2/
├── .git/
│   └── hooks/
│       ├── pre-commit
│       ├── post-commit
│       ├── pre-push
│       └── post-push
├── .github/
│   └── workflows/
│       └── ci.yml
├── docker-compose.yml
├── app.py
├── requirements.txt
├── test_basic.py
└── README.md
```

---

## Cómo se ejecutan los tests

### Tests con pytest

```bash
pytest -v
```

### Descripción de los tests

* **Tests unitarios:** verifican la creación, consulta y eliminación de pacientes.
* **Tests de integración:** prueban las peticiones HTTP contra los endpoints del microservicio.
* Todos los tests pasan correctamente, asegurando el funcionamiento del sistema.

Ejemplo de salida esperada:

```
============================= test session starts =============================
collected 3 items

test_basic.py::test_registrar_paciente PASSED
test_basic.py::test_consultar_paciente PASSED
test_basic.py::test_eliminar_paciente PASSED
============================== 3 passed in 0.42s ==============================
```

---

## Qué hacen los hooks configurados

El proyecto incluye 4 Git hooks locales ubicados en `.git/hooks/` que automatizan la validación del código.

### 1. Pre-commit Hook

*Archivo:* `.git/hooks/pre-commit`
**Acciones automáticas:**

* Verifica formato con `black`
* Ejecuta `flake8` para linting
* Lanza `pytest` para asegurar que todos los tests pasan
* *Bloquea el commit* si alguna verificación falla

**Cuándo se ejecuta:** antes de cada commit.

---

### 2. Post-commit Hook

*Archivo:* `.git/hooks/post-commit`
**Acciones automáticas:**

* Registra la información del commit (autor, hash y mensaje) en `commit_log.txt`
* Guarda la fecha y hora de la confirmación
* Permite mantener un historial local de commits

**Cuándo se ejecuta:** después de un commit exitoso.

---

### 3. Pre-push Hook

*Archivo:* `.git/hooks/pre-push`
**Acciones automáticas:**

* Ejecuta `pytest -v` antes del envío al repositorio remoto
* *Aborta el push* si algún test falla

**Cuándo se ejecuta:** justo antes de ejecutar `git push`.

---

### 4. Post-push Hook

*Archivo:* `.git/hooks/post-push`
**Acciones automáticas:**

* Muestra un mensaje de confirmación en consola tras un push exitoso
* Informa del último commit enviado

**Cuándo se ejecuta:** después del push.

---

## Pipeline CI/CD con GitHub Actions

El proyecto incluye un workflow automatizado definido en `.github/workflows/ci.yml` para asegurar calidad y despliegue continuo.

### ¿Cuándo se ejecuta?

* En cada *push* o *pull request* a la rama `main`.

### Jobs del pipeline

#### 1. **Job Test**

* Configura un entorno con Python 3.11.
* Instala dependencias desde `requirements.txt`.
* Ejecuta la suite de tests completa con pytest.
* Si los tests fallan, el flujo se detiene.

#### 2. **Job Build & Deploy**

* Solo se ejecuta si el *Job Test* finaliza correctamente.
* Construye la imagen Docker del microservicio.
* Despliega la aplicación en un contenedor local (runner) de GitHub Actions.
* Comprueba que el servicio responde en el puerto 8000.

### Flujo completo

```
Push a main → Test → Build → Deploy → Verificación → ✅
```

### Ventajas del pipeline

* Automatización completa sin intervención manual.
* Garantía de calidad: solo se despliega código que pasa todos los tests.
* Reproducibilidad: mismo entorno de ejecución en cada push.
* Feedback inmediato sobre errores o fallos en integración.

---

## Comandos útiles

```bash
# Ejecutar la aplicación localmente
uvicorn app:app --reload

# Ejecutar los tests
pytest -v

# Detener contenedores
docker-compose down

# Ver logs de ejecución
docker-compose logs
```

---

## Enlace al repositorio de GitHub

[https://github.com/adriannlm/practica1-DYA.git](https://github.com/adriannlm/practica1-DYA.git)

---
