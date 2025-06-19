# KIBA

Aplicación de gestión de citas y envío de SMS basada en **Flask** y **React**.
Incluye autenticación por JWT y base de datos PostgreSQL.

## Variables de entorno

Configure un archivo `.env` a partir de `.env.example` con al menos:

- `DATABASE_URL` – cadena de conexión para SQLAlchemy.
- `JWT_SECRET` – clave secreta para firmar tokens.
- `HABLAME_ACCOUNT`, `HABLAME_APIKEY`, `HABLAME_TOKEN` – credenciales del servicio SMS.
- `FRONTEND_URL` – origen permitido para CORS.
- `ADMIN_EMAIL` y `ADMIN_PASS` – datos del administrador inicial.
- `SENTRY_DSN` – opcional, para reportar errores.

## Desarrollo del backend

Instale las dependencias y ejecute el servidor:

```bash
pip install -r requirements.txt
python manage.py runserver
```

La API estará disponible en `http://localhost:5000/`.

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

## Uso de MySQL de XAMPP en Windows 10

Si trabajas en Windows 10 con XAMPP puedes utilizar el servicio de MySQL que
viene incluido. Instala el conector de MySQL para Python antes de ejecutar el
servidor:

```bash
pip install PyMySQL
```

En tu archivo `.env` configura `DATABASE_URL` con una cadena similar a la
siguiente (ajusta usuario, contraseña y base según corresponda):

```env
DATABASE_URL=mysql+pymysql://root:@localhost:3306/kiba
```

Al arrancar `mysqld` desde el panel de XAMPP podrás usar `python manage.py
runserver` normalmente.

## Despliegue en Render

Ejemplo de configuración para el servicio:

```json
{
  "buildCommand": "pip install -r requirements.txt && cd frontend && npm install && npm run build",
  "startCommand": "gunicorn backend.app.main:app --bind 0.0.0.0:$PORT"
}
```

Asegúrese de definir en el panel de Render todas las variables de entorno necesarias.
