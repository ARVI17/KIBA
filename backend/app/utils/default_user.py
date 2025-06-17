import os
from backend.app.config import db
from backend.app.models.user import Usuario, Rol


def seed_default_admin():
    """Create default admin user if credentials are provided."""
    admin_email = os.getenv("DEFAULT_ADMIN_EMAIL")
    admin_password = os.getenv("DEFAULT_ADMIN_PASSWORD")

    if not admin_email or not admin_password:
        return

    if Usuario.query.filter_by(correo=admin_email).first():
        return

    admin_role = Rol.query.filter_by(nombre="Administrador").first()
    if not admin_role:
        admin_role = Rol(nombre="Administrador")
        db.session.add(admin_role)
        db.session.commit()

    user = Usuario(correo=admin_email, rol=admin_role)
    user.set_contrasena(admin_password)
    db.session.add(user)
    db.session.commit()
