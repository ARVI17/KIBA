# KIBA/manage.py
import os
from dotenv import load_dotenv

load_dotenv()

from backend.app.main import app
from backend.app.config import db
from backend.app.models.user import Usuario, Rol
from backend.app.models.sms import Especialidad
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


# Configura Migrate
migrate = Migrate(app, db)


# Configura Manager
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def crear_tablas():
    """Crear tablas de la base de datos."""
    with app.app_context():
        db.create_all()
        print("✅ Tablas creadas correctamente en la base de datos.")


@manager.command
def cargar_datos():
    """Carga datos de ejemplo en la base de datos."""
    with app.app_context():
        if not Rol.query.first():
            admin_role = Rol(nombre='Administrador')
            operator_role = Rol(nombre='Operador')
            db.session.add(admin_role)
            db.session.add(operator_role)

        if not Especialidad.query.first():
            especialidades = ['Ortopedia', 'Medicina Interna', 'Pediatría', 'Cardiología']
            for esp in especialidades:
                nueva = Especialidad(nombre=esp)
                db.session.add(nueva)

        if not Usuario.query.filter_by(correo='admin@kiba.com').first():
            admin = Usuario(
                correo='admin@kiba.com',
                rol_id=1
            )
            admin.set_contrasena('admin123')
            db.session.add(admin)

        db.session.commit()
        print('✅ Datos iniciales cargados correctamente en la base de datos.')

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ['1', 'true', 't', 'yes']
    app.run(host='0.0.0.0', debug=debug_mode, port=5000)
