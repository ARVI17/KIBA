# backend/app/main.py

import os
from backend.app.config import create_app, db
from backend.app.models.user import Usuario, Rol
from backend.app.models.sms import Especialidad, SMS, Confirmacion
from backend.app.routes.auth import auth_bp
from backend.app.models.sms_pendiente import SMSPendiente
from backend.app.routes.specialty import specialty_bp
from backend.app.routes.paciente import paciente_bp
from backend.app.routes.cita import cita_bp
from flask_migrate import Migrate
from backend.app.routes.confirmacion import confirmacion_bp
from backend.app.routes.sms import sms_bp


# Ensure SECRET_KEY exists when running the development server directly
os.environ.setdefault('SECRET_KEY', 'kiba-insecure-secret')

app = create_app()
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(specialty_bp, url_prefix='/api')
app.register_blueprint(paciente_bp, url_prefix='/api')
app.register_blueprint(cita_bp, url_prefix='/api')
app.register_blueprint(sms_bp, url_prefix='/api')
migrate = Migrate(app, db)
app.register_blueprint(confirmacion_bp, url_prefix='/api')


@app.route('/')
def home():
    return 'KIBA Backend funcionando correctamente ✅'

#⚠️ Ruta desactivada por seguridad
# @app.route('/crear-tablas')
# def crear_tablas():
#         db.create_all()
#         return '✅ Tablas creadas correctamente en la base de datos.'

# ⚠️ Código para cargar datos de ejemplo disponible como comando CLI en manage.py

import os

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ['1', 'true', 't', 'yes']
    app.run(debug=debug_mode, port=5000)
