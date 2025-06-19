# backend/app/config.py

import logging
import os


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

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Create and configure the Flask application."""
    load_dotenv()

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["SECRET_KEY"] = os.environ["JWT_SECRET"]
    app.config["SENTRY_DSN"] = SENTRY_DSN

    register_error_handlers(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

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
        return "KIBA Backend funcionando correctamente ✅"

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    return app
