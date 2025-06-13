# KIBA

## Environment Variables

The backend relies on several environment variables:

- `DATABASE_URL` &ndash; SQLAlchemy connection string for the application's database.
- `JWT_SECRET` &ndash; secret used to sign JWTs and Flask sessions.
- `API_HABLAME_KEY` &ndash; API key for the Hablame SMS API (real or dummy).
- `FRONTEND_URL` &ndash; URL where the React frontend is served.
- `BACKEND_URL` &ndash; base URL for the Flask API.

A `.env.example` file contains these variables with placeholder values. Copy it to
`.env` and edit it with your credentials. Make sure the variables are loaded
before running the application.

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
