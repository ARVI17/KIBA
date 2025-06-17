import logging
import os
from backend.app.config import db
from backend.app.models.user import Usuario, Rol

logger = logging.getLogger(__name__)


def seed_default_admin():
    """Create default admin user if credentials are provided."""
    admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
    admin_password = os.getenv("ADMIN_PASS", "Admin123!")
    try:
        if not Usuario.query.filter_by(correo=admin_email).first():
            admin_role = Rol.query.filter_by(nombre="Administrador").first()
            if not admin_role:
                admin_role = Rol(nombre="Administrador")
                db.session.add(admin_role)
                db.session.commit()

            user = Usuario(correo=admin_email, rol=admin_role)
            user.set_contrasena(admin_password)
            db.session.add(user)
            db.session.commit()
            logger.info("Usuario admin por defecto sembrado: %s", admin_email)
    except Exception:
        logger.exception("Fallo al sembrar el usuario admin por defecto")
