import os
from dotenv import load_dotenv

load_dotenv()

from backend.app.main import app
from backend.app.config import db
from backend.app.models.user import Usuario, Rol
from backend.app.models.sms import Especialidad
from flask_migrate import Migrate
from flask_script import Manager

# Inicializar migraciones y comandos de script
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', migrate)

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
        # Roles
        if not Rol.query.first():
            admin_role = Rol(nombre='Administrador')
            operator_role = Rol(nombre='Operador')
            db.session.add_all([admin_role, operator_role])

        # Especialidades
        if not Especialidad.query.first():
            especialidades = ['Ortopedia', 'Medicina Interna', 'Pediatría', 'Cardiología']
            for esp in especialidades:
                db.session.add(Especialidad(nombre=esp))

        # Usuario admin
        if not Usuario.query.filter_by(correo='admin@kiba.com').first():
            admin = Usuario(correo='admin@kiba.com', rol_id=1)
            admin.set_contrasena('admin123')
            db.session.add(admin)

        db.session.commit()
        print('✅ Datos iniciales cargados correctamente en la base de datos.')

if __name__ == '__main__':
    manager.run()
