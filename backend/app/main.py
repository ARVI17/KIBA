# backend/app/main.py
import logging
import os
from dotenv import load_dotenv
from flask_cors import CORS
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from sentry_sdk import init as sentry_init
from sentry_sdk.integrations.flask import FlaskIntegration

from backend.app.config import create_app, db
from backend.app.models.user import Usuario, Rol
from backend.app.models.sms import Especialidad, SMS
from backend.app.models.confirmacion import Confirmacion
from backend.app.models.sms_pendiente import SMSPendiente
from backend.app.routes.auth import auth as auth_bp
from backend.app.routes.specialty import specialty_bp
from backend.app.routes.paciente import paciente_bp
from backend.app.routes.cita import cita_bp
from backend.app.routes.sms import sms_bp
from backend.app.routes.confirmacion import confirmacion_bp
from backend.app.utils.default_user import seed_default_admin
from flask_migrate import Migrate

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger("backend")

# Carga variables de entorno
load_dotenv()
logger.info("Arrancando KIBA")

# Crear app y configurar extensiones
app = create_app()
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configurar Sentry si está habilitado
dsn = app.config.get("SENTRY_DSN")
if dsn:
    sentry_init(
        dsn=dsn,
        integrations=[FlaskIntegration()],
        traces_sample_rate=0.1
    )

# Exponer métricas Prometheus en /metrics
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/metrics": make_wsgi_app()
})

# Inicializar DB y migraciones
db.init_app(app)
migrate = Migrate(app, db)

# Registrar blueprints
for bp in [
    auth_bp,
    specialty_bp,
    paciente_bp,
    cita_bp,
    sms_bp,
    confirmacion_bp
]:
    app.register_blueprint(bp, url_prefix="/api")

# Sembrar datos iniciales (admin, roles, especialidades)
with app.app_context():
    seed_default_admin()

# Rutas básicas
@app.route("/")
def home():
    return 'KIBA Backend funcionando correctamente ✅'

@app.route("/health")
def health():
    return {"status": "ok"}, 200

# Punto de entrada
if __name__ == "__main__":
    debug_flag = os.environ.get('FLASK_DEBUG', '').lower() in ['1', 'true', 't', 'yes']
    app.run(host='0.0.0.0', port=5000, debug=debug_flag)
# Exponer la app para Gunicorn
application = app   # Para compatibilidad con WSGI