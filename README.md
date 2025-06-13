# KIBA

## Environment Variables

The backend relies on several environment variables:

- `DATABASE_URL` &ndash; SQLAlchemy connection string for the application's database.
- `HABLAME_ACCOUNT` &ndash; account identifier for the Hablame SMS API.
- `HABLAME_APIKEY` &ndash; API key for the Hablame SMS API.
- `HABLAME_TOKEN` &ndash; authentication token for the Hablame SMS API.
- `SECRET_KEY` &ndash; secret used to sign JWTs and Flask sessions. Defaults to `kiba-insecure-secret`.

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
