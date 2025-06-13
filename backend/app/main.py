# backend/app/main.py

import os
from dotenv import load_dotenv
from flask_cors import CORS
from backend.app.config import create_app, db
from backend.app.models.user import Usuario, Rol
from backend.app.models.sms import Especialidad, SMS
from backend.app.models.confirmacion import Confirmacion
from backend.app.routes.auth import auth_bp
from backend.app.models.sms_pendiente import SMSPendiente
from backend.app.routes.specialty import specialty_bp
from backend.app.routes.paciente import paciente_bp
from backend.app.routes.cita import cita_bp
from flask_migrate import Migrate
from backend.app.routes.confirmacion import confirmacion_bp
from backend.app.routes.sms import sms_bp

load_dotenv()

app = create_app()
CORS(app, origins=os.getenv('FRONTEND_URL'))
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

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ['1', 'true', 't', 'yes']
    app.run(host='0.0.0.0', debug=debug_mode, port=5000)
