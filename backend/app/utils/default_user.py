from backend.app.config import db
from backend.app.models.user import Usuario, Rol


def seed_default_admin():
    """Create default admin user if it doesn't exist."""
    admin_email = "admin@example.com"
    if Usuario.query.filter_by(correo=admin_email).first():
        return

    admin_role = Rol.query.filter_by(nombre="Administrador").first()
    if not admin_role:
        admin_role = Rol(nombre="Administrador")
        db.session.add(admin_role)
        db.session.commit()

    user = Usuario(correo=admin_email, rol=admin_role)
    user.set_contrasena("Admin123!")
    db.session.add(user)
    db.session.commit()
