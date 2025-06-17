# backend/app/main.py

import logging
import os
from dotenv import load_dotenv
from backend.app.config import create_app, db
from backend.app.models.user import Usuario, Rol
from backend.app.utils.default_user import seed_default_admin
from backend.app.models.sms import Especialidad, SMS
from backend.app.models.confirmacion import Confirmacion
from backend.app.routes.auth import auth

logger = logging.getLogger(__name__)
from backend.app.models.sms_pendiente import SMSPendiente
from backend.app.routes.specialty import specialty_bp
from backend.app.routes.paciente import paciente_bp
from backend.app.routes.cita import cita_bp
from flask_migrate import Migrate
from backend.app.routes.confirmacion import confirmacion_bp
from backend.app.routes.sms import sms_bp

load_dotenv()

logger.info("Arrancando Kiba")

app = create_app()
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

#⚠️ Ruta desactivada por seguridad
# @app.route('/crear-tablas')
# def crear_tablas():
#         db.create_all()
#         return '✅ Tablas creadas correctamente en la base de datos.'

# ⚠️ Código para cargar datos de ejemplo disponible como comando CLI en manage.py

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ['1', 'true', 't', 'yes']
    app.run(host='0.0.0.0', debug=debug_mode, port=5000)
