# Usamos una imagen base de Python 3.11
FROM python:3.11

# Evita que Poetry cree entornos virtuales separados
ENV POETRY_VIRTUALENVS_CREATE=false

# Instalamos el cliente de PostgreSQL y limpiamos caches de apt
RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client && rm -rf /var/lib/apt/lists/*

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos archivos de dependencias
COPY pyproject.toml poetry.lock* /app/

# Instalamos Poetry y las dependencias del proyecto
RUN pip install --no-cache-dir poetry && poetry install --no-root --no-interaction --no-ansi

# Copiamos el resto del código de la aplicación
COPY . /app

# Exponemos el puerto usado por la API
EXPOSE 8000

# Comando por defecto para iniciar la aplicación
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
