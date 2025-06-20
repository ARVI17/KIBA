# backend/app/config.py
# backend/app/config.py
import logging
import os
from urllib.parse import urlparse

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from dotenv import load_dotenv
from sentry_sdk import init as sentry_init
from sentry_sdk.integrations.flask import FlaskIntegration

# Load environment variables from .env as soon as the module is imported
load_dotenv()

_env_url = os.getenv("DATABASE_URL")
if not _env_url or not (
    _env_url.startswith("postgres://") or _env_url.startswith("postgresql://")
):
    raise RuntimeError(
        "DATABASE_URL debe definirse y usar el esquema de PostgreSQL"
    )

from backend.app.error_handlers import register_error_handlers
from backend.app.cli import register_cli

# Cargar variables de entorno lo antes posible
load_dotenv()

# Leer la URL de la base de datos desde .env
def _build_database_uri():
    url = os.getenv("DATABASE_URL", "")
    # Ajuste automático de mysql:// a mysql+pymysql://
    if url.startswith("mysql://"):
        url = url.replace("mysql://", "mysql+pymysql://", 1)
    return url

# URL de la base de datos ya con variables cargadas
SQLALCHEMY_DATABASE_URI = _build_database_uri()
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuración de Sentry
SENTRY_DSN = os.getenv("SENTRY_DSN", None)

# Logging básico
t_log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, t_log_level, logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)

if not SQLALCHEMY_DATABASE_URI:
    logger.warning("La variable de entorno DATABASE_URL no est\xC3\xA1 definida")
if not SENTRY_DSN:
    logger.info("SENTRY_DSN no definido, Sentry deshabilitado")

# Mostrar URL de conexión (hostname:port/db)
_parsed = urlparse(SQLALCHEMY_DATABASE_URI)
_masked = f"{_parsed.scheme}://{_parsed.hostname or ''}"
if _parsed.port:
    _masked += f":{_parsed.port}"
if _parsed.path:
    _masked += _parsed.path
logger.info("Usando DATABASE_URL: %s", _masked)

db = SQLAlchemy()
migrate = Migrate()

# Factory de aplicación
def create_app():
    """Create and configure the Flask application."""

    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=db_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=SQLALCHEMY_TRACK_MODIFICATIONS,
        SECRET_KEY=secret_key,
        SENTRY_DSN=SENTRY_DSN,
    )

    # Inicializar extensiones y registrar manejadores de error
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    register_error_handlers(app)
    register_cli(app)

    if app.config.get("SENTRY_DSN"):
        sentry_init(
            dsn=app.config["SENTRY_DSN"],
            integrations=[FlaskIntegration()],
            traces_sample_rate=0.1,
        )

    # Expose Prometheus metrics
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})

    # Register blueprints
    from backend.app.routes.auth import auth
    from backend.app.routes.specialty import specialty_bp
    from backend.app.routes.paciente import paciente_bp
    from backend.app.routes.cita import cita_bp
    from backend.app.routes.sms import sms_bp
    from backend.app.routes.confirmacion import confirmacion_bp

    app.register_blueprint(auth, url_prefix="/api")
    app.register_blueprint(specialty_bp, url_prefix="/api")
    app.register_blueprint(paciente_bp, url_prefix="/api")
    app.register_blueprint(cita_bp, url_prefix="/api")
    app.register_blueprint(sms_bp, url_prefix="/api")
    app.register_blueprint(confirmacion_bp, url_prefix="/api")

    from backend.app.utils.default_user import seed_default_admin
    with app.app_context():
        seed_default_admin()

    @app.route("/")
    def home():
        return "CitaMatic Backend funcionando correctamente ✅"

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    return app


