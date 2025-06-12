import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app.config import create_app, db
from backend.app.routes.sms import sms_bp
from backend.app.models.user import Usuario, Rol
from backend.app.utils.token_manager import generar_token

@pytest.fixture
def app():
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    app = create_app()
    app.register_blueprint(sms_bp, url_prefix='/api')
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        # seed a default user for auth tests
        admin_role = Rol(nombre='Test')
        db.session.add(admin_role)
        user = Usuario(correo='test@example.com', rol=admin_role)
        user.set_contrasena('password')
        db.session.add(user)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(app):
    with app.app_context():
        user = Usuario.query.first()
        token = generar_token(user)
    return {'Authorization': token}
