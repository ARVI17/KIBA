import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.config import create_app, db
from backend.app.routes.sms import sms_bp
from backend.app.routes.auth import auth
from backend.app.routes.confirmacion import confirmacion_bp
from backend.app.routes.cita import cita_bp


@pytest.fixture
def app():
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    os.environ["JWT_SECRET"] = "testsecret"
    app = create_app()
    app.register_blueprint(sms_bp, url_prefix="/api")
    app.register_blueprint(auth, url_prefix="/api")
    app.register_blueprint(confirmacion_bp, url_prefix="/api")
    app.register_blueprint(cita_bp, url_prefix="/api")
    app.config["TESTING"] = True
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
