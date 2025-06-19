# backend/app/config.py

import logging
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse

from backend.app.error_handlers import register_error_handlers

# Ajuste automático de esquema para pg8000 o psycopg2
url = os.getenv("DATABASE_URL", "")
if url.startswith("postgres://"):
    # si usas pg8000:
    url = url.replace("postgres://", "postgresql+pg8000://", 1)
    # o si prefieres psycopg2, comenta la línea anterior y descomenta:
    # url = url.replace("postgres://", "postgresql+psycopg2://", 1)

SQLALCHEMY_DATABASE_URI = url
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuración de Sentry
SENTRY_DSN = os.getenv("SENTRY_DSN", None)

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)
_parsed = urlparse(SQLALCHEMY_DATABASE_URI)
_masked = f"{_parsed.scheme}://{_parsed.hostname or ''}"
if _parsed.port:
    _masked += f":{_parsed.port}"
if _parsed.path:
    _masked += _parsed.path
logger.info("Usando DATABASE_URL: %s", _masked)

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["SECRET_KEY"] = os.environ["JWT_SECRET"]
    app.config["SENTRY_DSN"] = SENTRY_DSN

    register_error_handlers(app)

    return app
