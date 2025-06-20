import os
import sys
import pytest

# Ensure valid DATABASE_URL before importing the config module
os.environ.setdefault("DATABASE_URL", "postgresql://user:pass@localhost/db")
os.environ.setdefault("SECRET_KEY", "testsecret")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import backend.app.config as config
db = config.db
from backend.app.models.user import Rol, Usuario


@pytest.fixture
def app():
    os.environ["DATABASE_URL"] = "postgresql://user:pass@localhost/db"
    os.environ["SECRET_KEY"] = "testsecret"
    config.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    app = config.create_app()
    app.config["TESTING"] = True
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def seed_user(app):
    """Seed default roles and a test user."""
    with app.app_context():
        admin_role = Rol(nombre="Administrador")
        operator_role = Rol(nombre="Operador")
        db.session.add_all([admin_role, operator_role])
        user = Usuario(correo="user@example.com", rol=admin_role)
        user.set_contrasena("secret123")
        db.session.add(user)
        db.session.commit()
        return user
