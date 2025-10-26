FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5006

# Asegurar que la app se ejecuta en modo producción
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Permitir todos los orígenes en desarrollo
ENV CORS_ORIGINS="*"

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5006", "--reload"]