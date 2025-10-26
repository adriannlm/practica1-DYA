# Guía de Despliegue

## Requisitos Previos

- Docker y Docker Compose instalados
- Git instalado
- Acceso a GitHub

## Pasos para el Despliegue

1. **Clonar el Repositorio**
   ```bash
   git clone https://github.com/adriannlm/practica1-DYA.git
   cd practica1-DYA
   ```

2. **Configurar Variables de Entorno**
   - Crear archivo `.env` en la raíz del proyecto:
     ```env
     DB_HOST=db
     DB_NAME=clinica
     DB_USER=admin
     DB_PASS=admin
     SECRET_KEY=tu_clave_secreta_muy_segura
     ```

3. **Construir y Ejecutar los Contenedores**
   ```bash
   docker-compose up --build -d
   ```

4. **Verificar el Despliegue**
   - Backend: http://localhost:8000
   - Frontend: http://localhost:3000
   - Documentación API: http://localhost:8000/docs

5. **Monitorizar los Logs**
   ```bash
   docker-compose logs -f
   ```

## Mantenimiento

### Actualizar la Aplicación
```bash
git pull
docker-compose down
docker-compose up --build -d
```

### Backup de la Base de Datos
```bash
docker exec practica1-db pg_dump -U admin clinica > backup.sql
```

### Restaurar la Base de Datos
```bash
cat backup.sql | docker exec -i practica1-db psql -U admin -d clinica
```

## Solución de Problemas

1. **Error de Conexión a la Base de Datos**
   ```bash
   docker-compose down
   docker volume rm practica1_db-data
   docker-compose up -d
   ```

2. **Limpiar Todo y Reiniciar**
   ```bash
   docker-compose down -v
   docker-compose up --build -d
   ```

## CI/CD

El proyecto utiliza GitHub Actions para:
- Ejecutar tests automáticamente
- Construir imágenes Docker
- Verificar la calidad del código

Los workflows se ejecutan en:
- Push a main o develop
- Pull Requests a main o develop