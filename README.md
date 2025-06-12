# KIBA

## Environment Variables

The backend relies on several environment variables:

- `DATABASE_URL` &ndash; SQLAlchemy connection string for the application's database.
- `HABLAME_ACCOUNT` &ndash; account identifier for the Hablame SMS API.
- `HABLAME_APIKEY` &ndash; API key for the Hablame SMS API.
- `HABLAME_TOKEN` &ndash; authentication token for the Hablame SMS API.
- `SECRET_KEY` &ndash; secret used to sign JWTs and Flask sessions. Defaults to `kiba-insecure-secret`.

Make sure these variables are defined before running the application.

## Backend Development

Install Python dependencies for the backend:

```bash
pip install -r requirements.txt
```

Set the required environment variables (`DATABASE_URL`, `SECRET_KEY`, etc.) and
start the development server:

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
