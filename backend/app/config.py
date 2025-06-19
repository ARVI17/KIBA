# backend/app/config.py
# backend/app/config.py
import logging
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse
from pathlib import Path

# Carga de variables de entorno (si no se ha cargado antes)
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parents[2] / '.env')

# Leer la URL de la base de datos desde .env
def _build_database_uri():
    url = os.getenv("DATABASE_URL", "")
    # Ajuste automático de mysql:// a mysql+pymysql://
    if url.startswith("mysql://"):
        url = url.replace("mysql://", "mysql+pymysql://", 1)
    return url

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

# Mostrar URL de conexión (hostname:port/db)
_parsed = urlparse(SQLALCHEMY_DATABASE_URI)
_masked = f"{_parsed.scheme}://{_parsed.hostname or ''}"
if _parsed.port:
    _masked += f":{_parsed.port}"
if _parsed.path:
    _masked += _parsed.path
logger.info("Usando DATABASE_URL: %s", _masked)

# Instancia de la base de datos
db = SQLAlchemy()

# Factory de aplicación
def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=SQLALCHEMY_TRACK_MODIFICATIONS,
        SECRET_KEY=os.getenv("JWT_SECRET", ""),
        SENTRY_DSN=SENTRY_DSN,
    )

    # Inicializar extensiones
    db.init_app(app)

    # Registrar manejadores de error
    from backend.app.error_handlers import register_error_handlers
    register_error_handlers(app)

    return app


# backend/app/error_handlers.py
from flask import jsonify
from flask import Flask
from werkzeug.exceptions import HTTPException
import logging

logger = logging.getLogger(__name__)

def register_error_handlers(app: Flask) -> None:
    """Registra manejadores HTTP y genéricos para la app."""
    @app.errorhandler(HTTPException)
    def handle_http_error(e: HTTPException):
        return jsonify(error=e.description), e.code

    @app.errorhandler(Exception)
    def handle_exception(e: Exception):
        logger.error("Unhandled exception", exc_info=True)
        return jsonify(error="Internal server error"), 500

    # Errores HTTP comunes explícitos
def register_specific_handlers(app: Flask) -> None:
    codes = {
        400: "Bad request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not found",
        405: "Method not allowed",
        422: "Unprocessable entity",
        429: "Too many requests",
        503: "Service unavailable",
        504: "Gateway timeout",
        501: "Not implemented",
        418: "I'm a teapot",
    }
    for code, msg in codes.items():
        @app.errorhandler(code)
        def handler(e, _msg=msg, _code=code):
            return jsonify(error=_msg), _code

    # Registrar específicos
    register_specific_handlers(app)
    # Registrar manejadores de error específicos
    register_error_handlers(app)
    # Registrar manejadores de error genéricos
    register_error_handlers(app)    
    # Registrar manejadores de error HTTP   
    register_error_handlers(app)
    # Registrar manejadores de error genéricos
    register_error_handlers(app)
    # Registrar manejadores de error HTTP
    register_error_handlers(app)
    # Registrar manejadores de error genéricos
    register_error_handlers(app)
    # Registrar manejadores de error HTTP
    register_error_handlers(app)
    # Registrar manejadores de error genéricos
    register_error_handlers(app)
