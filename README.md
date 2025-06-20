# CitaMatic

Aplicación de gestión de citas y envío de SMS basada en **Flask** y **React**.
PostgreSQL es la base de datos principal del proyecto e incluye autenticación por JWT.

## Variables de entorno

Copie el archivo `.env.example` a `.env` y complete con al menos:

- `DATABASE_URL` – cadena de conexión para SQLAlchemy.
- `SECRET_KEY` – clave secreta para firmar tokens (también se acepta `JWT_SECRET` o `JWT_SECRET_KEY`).
- `JWT_SECRET_KEY` – alternativa opcional a `SECRET_KEY`.
- `HABLAME_ACCOUNT` – identificador de la cuenta Hablame.
- `HABLAME_APIKEY` – ApiKey de la cuenta Hablame.
- `HABLAME_TOKEN` – token de autenticación para el servicio SMS.
- `FRONTEND_URL` – origen permitido para CORS (si falta se usa `*`).
- `ADMIN_EMAIL` y `ADMIN_PASS` – datos del administrador inicial.
- `SENTRY_DSN` – opcional, para reportar errores.

El archivo `.env.example` contiene ejemplos para PostgreSQL y MySQL. Elija una de las URLs y deje la otra comentada. 
## Base de datos (PostgreSQL por defecto)

Para desarrollo local utilizamos **PostgreSQL**. Cree la base de datos vacía y
aplique las migraciones iniciales con:


Ajuste `DATABASE_URL` en su `.env` para que apunte a la instancia creada.

## Configuración rápida sin Docker

Siga estos pasos para levantar el proyecto localmente sin utilizar contenedores:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask --app backend.app.main db upgrade
python manage.py cargar_datos
flask --app backend.app.main run
```

En otra terminal inicie el frontend:

```bash
cd frontend
npm install
npm run dev
```

## Desarrollo del backend

Instale las dependencias, aplique las migraciones y ejecute el servidor:

```bash
pip install -r requirements.txt
flask --app backend.app.main db upgrade
flask --app backend.app.main run
```

La API estará disponible en `http://localhost:5000/`.

### Herramientas de desarrollo opcionales

Para análisis estático puedes instalar manualmente `mypy` y `bandit`. Estas
dependencias no forman parte de `requirements.txt` para mantener liviano el
entorno de producción.

### Pre-commit

Para ejecutar Black, Flake8 y las herramientas de frontend antes de cada
commit instala los hooks con:

```bash
pre-commit install
```

## Desarrollo del frontend

Dentro de `frontend/` se encuentra el proyecto Vite + React:

```bash
cd frontend
npm install
npm run dev
```

Para generar los artefactos de producción:

```bash
npm run build
```

## Docker

Puede construir la imagen y levantar todo el entorno con:

```bash
docker-compose up --build
```

## Uso opcional con MySQL

Si prefieres MySQL puedes utilizar el servicio incluido en XAMPP u otra
instancia. Instala el conector `PyMySQL` para Python antes de ejecutar el
servidor:

```bash
pip install PyMySQL
```

En tu archivo `.env` configura `DATABASE_URL` con una cadena similar a la
siguiente (ajusta usuario, contraseña y base según corresponda):

```env
DATABASE_URL=mysql+pymysql://root:@localhost:3306/citamatic
```

Al arrancar `mysqld` desde el panel de XAMPP podrás usar `flask --app backend.app.main run` normalmente.

