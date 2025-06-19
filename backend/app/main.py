# backend/app/main.py

import logging
import os
from dotenv import load_dotenv
from backend.app.config import create_app, db
from backend.app.utils.default_user import seed_default_admin
from backend.app.routes.auth import auth
from flask_cors import CORS
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from sentry_sdk import init as sentry_init
from sentry_sdk.integrations.flask import FlaskIntegration

from backend.app.routes.specialty import specialty_bp
from backend.app.routes.paciente import paciente_bp
from backend.app.routes.cita import cita_bp
from flask_migrate import Migrate
from backend.app.routes.confirmacion import confirmacion_bp
from backend.app.routes.sms import sms_bp

# Logging unificado
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger("backend")

load_dotenv()

logger.info("Arrancando Kiba")

app = create_app()

# CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Sentry
if app.config.get("SENTRY_DSN"):
    sentry_init(
        dsn=app.config["SENTRY_DSN"],
        integrations=[FlaskIntegration()],
        traces_sample_rate=0.1
    )

# Exponer métricas Prometheus en /metrics
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/metrics": make_wsgi_app()
})

try:
    db.init_app(app)
    logger.info("Base de datos inicializada correctamente")
except Exception:
    logger.exception("Error al inicializar la base de datos")
    raise

app.register_blueprint(auth, url_prefix='/api')
app.register_blueprint(specialty_bp, url_prefix='/api')
app.register_blueprint(paciente_bp, url_prefix='/api')
app.register_blueprint(cita_bp, url_prefix='/api')
app.register_blueprint(sms_bp, url_prefix='/api')
migrate = Migrate(app, db)
app.register_blueprint(confirmacion_bp, url_prefix='/api')

with app.app_context():
    seed_default_admin()


@app.route('/')
def home():
    return 'KIBA Backend funcionando correctamente ✅'


@app.route('/health')
def health():
    return {"status": "ok"}, 200

#⚠️ Ruta desactivada por seguridad
# @app.route('/crear-tablas')
# def crear_tablas():
#         db.create_all()
#         return '✅ Tablas creadas correctamente en la base de datos.'

# ⚠️ Código para cargar datos de ejemplo disponible como comando CLI en manage.py

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ['1', 'true', 't', 'yes']
    app.run(host='0.0.0.0', debug=debug_mode, port=5000)
