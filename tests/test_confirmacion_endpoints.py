from backend.app.config import db
from backend.app.models.user import Rol, Usuario


def seed_user():
    admin_role = Rol(nombre="Administrador")
    operator_role = Rol(nombre="Operador")
    db.session.add_all([admin_role, operator_role])
    user = Usuario(correo="user@example.com", rol=admin_role)
    user.set_contrasena("secret123")
    db.session.add(user)
    db.session.commit()


def get_token(client, app):
    with app.app_context():
        seed_user()
    resp = client.post(
        "/api/login",
        json={"correo": "user@example.com", "contrasena": "secret123"},
    )
    return resp.get_json()["token"]


def test_confirmaciones_requires_token(client):
    resp = client.get("/api/confirmaciones")
    assert resp.status_code == 401


def test_confirmaciones_with_token(client, app):
    token = get_token(client, app)
    resp = client.get("/api/confirmaciones", headers={"Authorization": token})
    assert resp.status_code == 200
