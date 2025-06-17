# KIBA

## Environment Variables

The backend relies on several environment variables:

- `DATABASE_URL` &ndash; SQLAlchemy connection string for the application's database.
- `JWT_SECRET` &ndash; secret used to sign JWTs and Flask sessions.
- `HABLAME_ACCOUNT` &ndash; account identifier for the Hablame SMS API.
- `HABLAME_APIKEY` &ndash; API key for the Hablame SMS API.
- `HABLAME_TOKEN` &ndash; token for the Hablame SMS API.
- `FRONTEND_URL` &ndash; URL where the React frontend is served.
- `API_HABLAME_KEY` &ndash; legacy key, currently unused.
- `BACKEND_URL` &ndash; unused base URL variable.
- `DEFAULT_ADMIN_EMAIL` &ndash; email for the initial admin user created on startup.
- `DEFAULT_ADMIN_PASSWORD` &ndash; password for that user.

If these credentials are not provided, no admin account will be seeded automatically.

A `.env.example` file contains these variables with placeholder values. Copy it to
`.env` and edit it with your credentials. Ensure the variables are loaded
before running the application. When deploying on **Render**, add the same
variables in the dashboard so that the container starts correctly.

## Backend Development

Install the Python dependencies used by the backend (Flask, Flask-SQLAlchemy,
Flask-Migrate, etc.) using `requirements.txt`:

```bash
pip install -r requirements.txt
```

Ensure the variables from your `.env` file are loaded and start the development server:

```bash
python manage.py runserver
```

The API will be available at `http://localhost:5000/` by default.

## Frontend Development

The `frontend/` directory contains a Vite + React project.

Install dependencies and start the development server:

```bash
cd frontend
npm install
npm run dev
```

To build the production assets:

```bash
npm run build
```

The compiled files will appear in `frontend/dist`.

When deploying the React application to Vercel, set `VITE_API_URL` in the
project settings so that the frontend knows where to reach the backend API.

## Docker Usage

A `Dockerfile` is provided for the backend. Build the image with:

```bash
docker build -t kiba-backend .
```

Run the container exposing port `5000`:

```bash
docker run -p 5000:5000 kiba-backend
```

The repository also includes a `docker-compose.yml` to run both the backend and
the React frontend:

```bash
docker-compose up --build
```

The API will be available at `http://localhost:5000/` and the frontend at
`http://localhost:3000/`.

## Deploying on Render

Configure the service on [Render](https://render.com) with the following settings:

```json
{
  "buildCommand": "pip install -r requirements.txt && cd frontend && npm install && npm run build",
  "startCommand": "gunicorn backend.app.main:app"
}
```

Add the environment variables from `.env.sample` in the Render dashboard so that the container boots correctly.
