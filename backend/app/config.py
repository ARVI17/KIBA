# backend/app/config.py

import logging
import os
from urllib.parse import urlparse
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import HTTPException
from prometheus_client import make_wsgi_app
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

logger = logging.getLogger(__name__)
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # Database connection string
    db_uri = os.environ["DATABASE_URL"]
    parsed = urlparse(db_uri)
    logger.info("Conectando a Postgres en %s", parsed.hostname)
    if db_uri.startswith("postgres://"):
        db_uri = db_uri.replace("postgres://", "postgresql+pg8000://", 1)
    elif db_uri.startswith("postgresql://"):
        db_uri = db_uri.replace("postgresql://", "postgresql+pg8000://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Secret used to sign JWTs and sessions
    app.config['SECRET_KEY'] = os.environ['JWT_SECRET']

    CORS(app, origins=os.getenv('FRONTEND_URL'))

    sentry_dsn = os.getenv('SENTRY_DSN')
    if sentry_dsn:
        sentry_sdk.init(dsn=sentry_dsn, integrations=[FlaskIntegration()])

    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {'/metrics': make_wsgi_app()})

    db.init_app(app)

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
