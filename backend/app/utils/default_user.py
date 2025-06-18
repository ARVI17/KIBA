import logging
import os
from backend.app.config import db
from backend.app.models.user import Usuario, Rol

log = logging.getLogger("backend.seed")


def seed_default_admin():
    try:
        admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
        admin_password = os.getenv("ADMIN_PASS", "Admin123!")
        log.info("Comprobando existencia de admin %s", admin_email)
        usuario = Usuario.query.filter_by(correo=admin_email).first()
        if not usuario:
            log.info("Creando usuario admin por defecto")
            admin_role = Rol.query.filter_by(nombre="Administrador").first()
            if not admin_role:
                admin_role = Rol(nombre="Administrador")
                db.session.add(admin_role)
                db.session.commit()
            user = Usuario(correo=admin_email, rol=admin_role)
            user.set_contrasena(admin_password)
            db.session.add(user)
            db.session.commit()
        else:
            log.info("Usuario admin ya existe")
    except Exception:
        log.exception("Error al sembrar admin por defecto")
