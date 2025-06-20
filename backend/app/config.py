# backend/app/config.py
# -*- coding: utf-8 -*-
"""Configuración de la aplicación Flask para CitaMatic.
Este módulo configura la base de datos, extensiones, CORS, Sentry y rutas de la aplicación.
""" 
import logging
import os
from urllib.parse import urlparse

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from dotenv import load_dotenv
from sentry_sdk import init as sentry_init
from sentry_sdk.integrations.flask import FlaskIntegration

# Cargar variables de entorno desde .env
load_dotenv()

# Validar configuración de base de datos
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL or not (DATABASE_URL.startswith("postgres://") or DATABASE_URL.startswith("postgresql://")):
    raise RuntimeError("DATABASE_URL debe definirse y usar el esquema de PostgreSQL")

# Construir URI de SQLAlchemy
def _build_database_uri(url: str) -> str:
    # Ajuste automático de mysql:// a mysql+pymysql:// si fuera necesario
    if url.startswith("mysql://"):
        return url.replace("mysql://", "mysql+pymysql://", 1)
    return url

SQLALCHEMY_DATABASE_URI = _build_database_uri(DATABASE_URL)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Clave secreta de Flask
SECRET_KEY = os.getenv("SECRET_KEY") or os.getenv("JWT_SECRET")
if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY o JWT_SECRET debe definirse en las variables de entorno"
    )

# Configuración de Sentry
SENTRY_DSN = os.getenv("SENTRY_DSN") or None

# Logging básico
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)

# Mostrar URL de conexión (hostname:port/db) sin revelar credenciales completas
_parsed = urlparse(SQLALCHEMY_DATABASE_URI)
_masked = f"{_parsed.scheme}://{_parsed.hostname or ''}"
if _parsed.port:
    _masked += f":{_parsed.port}"
if _parsed.path:
    _masked += _parsed.path
logger.info("Usando DATABASE_URL: %s", _masked)
if not SENTRY_DSN:
    logger.info("SENTRY_DSN no definido, Sentry deshabilitado")

# Inicialización de extensiones
db = SQLAlchemy()
migrate = Migrate()

# Factory de la aplicación
def create_app():
    """Crea y configura la aplicación Flask."""
    required_vars = ["HABLAME_ACCOUNT", "HABLAME_APIKEY", "HABLAME_TOKEN"]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise RuntimeError(
            "Faltan variables de entorno: " + ", ".join(missing)
        )
    app = Flask(__name__)

    # Carga configuración
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=SQLALCHEMY_TRACK_MODIFICATIONS,
        SECRET_KEY=SECRET_KEY,
        SENTRY_DSN=SENTRY_DSN,
    )

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Configurar CORS
    frontend_url = os.getenv("FRONTEND_URL") or "*"
    if frontend_url == "*":
        logger.warning("FRONTEND_URL no establecido, usando '*' para CORS")
    CORS(app, resources={r"/api/*": {"origins": frontend_url}})

    # Registrar manejadores de error
    from backend.app.error_handlers import register_error_handlers
    register_error_handlers(app)

    # Registrar comandos CLI personalizados (evitando import circular)
    from backend.app.cli import register_cli
    register_cli(app)

    # Configurar Sentry si está definido
    if SENTRY_DSN:
        sentry_init(
            dsn=SENTRY_DSN,
            integrations=[FlaskIntegration()],
            traces_sample_rate=0.1,
        )

    # Exponer métricas de Prometheus
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})

    # Registrar blueprints
    from backend.app.routes.auth import auth
    from backend.app.routes.specialty import specialty_bp
    from backend.app.routes.paciente import paciente_bp
    from backend.app.routes.cita import cita_bp
    from backend.app.routes.sms import sms_bp
    from backend.app.routes.confirmacion import confirmacion_bp
    from backend.app.routes.health import health_bp

    app.register_blueprint(auth, url_prefix="/api")
    app.register_blueprint(specialty_bp, url_prefix="/api")
    app.register_blueprint(paciente_bp, url_prefix="/api")
    app.register_blueprint(cita_bp, url_prefix="/api")
    app.register_blueprint(sms_bp, url_prefix="/api")
    app.register_blueprint(confirmacion_bp, url_prefix="/api")
    app.register_blueprint(health_bp, url_prefix="/api")

    # Semilla de usuario admin por defecto
    from backend.app.utils.default_user import seed_default_admin
    with app.app_context():
        seed_default_admin()

    # Rutas de salud
    @app.route("/")
    def home():
        return "CitaMatic Backend funcionando correctamente ✅"

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    return app
