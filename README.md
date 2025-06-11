# KIBA

## Environment Variables

The backend relies on several environment variables:

- `DATABASE_URL` &ndash; SQLAlchemy connection string for the application's database.
- `HABLAME_ACCOUNT` &ndash; account identifier for the Hablame SMS API.
- `HABLAME_APIKEY` &ndash; API key for the Hablame SMS API.
- `HABLAME_TOKEN` &ndash; authentication token for the Hablame SMS API.
- `SECRET_KEY` &ndash; secret used to sign JWTs and Flask sessions. Defaults to `kiba-insecure-secret`.

Make sure these variables are defined before running the application.
