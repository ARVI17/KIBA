import click
from flask.cli import with_appcontext

from backend.app.config import db
from backend.app.models.user import Usuario, Rol
from backend.app.models.sms import Especialidad


@click.command('crear-tablas')
@with_appcontext
def crear_tablas():
    """Crear tablas de la base de datos."""
    db.create_all()
    click.echo("✅ Tablas creadas correctamente en la base de datos.")


@click.command('cargar-datos')
@with_appcontext
def cargar_datos():
    """Carga datos de ejemplo en la base de datos."""
    if not Rol.query.first():
        admin_role = Rol(nombre='Administrador')
        operator_role = Rol(nombre='Operador')
        db.session.add(admin_role)
        db.session.add(operator_role)

    if not Especialidad.query.first():
        especialidades = ['Ortopedia', 'Medicina Interna', 'Pediatría', 'Cardiología']
        for esp in especialidades:
            db.session.add(Especialidad(nombre=esp))

    if not Usuario.query.filter_by(correo='admin@kiba.com').first():
        admin = Usuario(correo='admin@kiba.com', rol_id=1)
        admin.set_contrasena('admin123')
        db.session.add(admin)

    db.session.commit()
    click.echo('✅ Datos iniciales cargados correctamente en la base de datos.')


def register_cli(app):
    app.cli.add_command(crear_tablas)
    app.cli.add_command(cargar_datos)
