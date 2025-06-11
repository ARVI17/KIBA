# backend/app/main.py

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
@app.route('/crear-tablas')
def crear_tablas():
        db.create_all()
        return '✅ Tablas creadas correctamente en la base de datos.'

# ⚠️ Ruta desactivada por seguridad
# @app.route('/cargar-datos')
# def cargar_datos():
#     if not Rol.query.first():
#         admin_role = Rol(nombre='Administrador')
#         operator_role = Rol(nombre='Operador')
#         db.session.add(admin_role)
#         db.session.add(operator_role)

#     if not Especialidad.query.first():
#         especialidades = ['Ortopedia', 'Medicina Interna', 'Pediatría', 'Cardiología']
#         for esp in especialidades:
#             nueva = Especialidad(nombre=esp)
#             db.session.add(nueva)

#     if not Usuario.query.filter_by(correo='admin@kiba.com').first():
#         admin = Usuario(
#             correo='admin@kiba.com',
#             contrasena='admin123',
#             rol_id=1
#         )
#         db.session.add(admin)

#     db.session.commit()
#     return '✅ Datos iniciales cargados correctamente en la base de datos.'

if __name__ == '__main__':
    app.run(debug=True, port=5000)
