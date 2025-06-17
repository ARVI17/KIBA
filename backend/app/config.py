# backend/app/config.py

import logging
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)
logger.info("Usando DATABASE_URL: %s", os.getenv("DATABASE_URL"))

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # Database connection string
    db_uri = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Secret used to sign JWTs and sessions
    app.config['SECRET_KEY'] = os.environ['JWT_SECRET']

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
