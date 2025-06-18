# backend/app/config.py

import logging
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException

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
logger.info("Usando DATABASE_URL: %s", SQLALCHEMY_DATABASE_URI)

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["SECRET_KEY"] = os.environ["JWT_SECRET"]
    app.config["SENTRY_DSN"] = SENTRY_DSN

    register_error_handlers(app)

    return app


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(HTTPException)
    def handle_http_error(e: HTTPException):
        return jsonify(error=e.description), e.code

    @app.errorhandler(Exception)
    def handle_exception(e: Exception):
        logger.error("Unhandled exception", exc_info=True)
        return jsonify(error="Internal server error"), 500
