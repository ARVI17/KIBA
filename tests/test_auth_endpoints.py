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


def test_login_success(client, app):
    with app.app_context():
        seed_user()
    resp = client.post(
        "/api/login",
        json={"correo": "user@example.com", "contrasena": "secret123"},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert "token" in data
    assert data["rol"] == "Administrador"


def test_login_invalid_password(client, app):
    with app.app_context():
        seed_user()
    resp = client.post(
        "/api/login",
        json={"correo": "user@example.com", "contrasena": "wrong"},
    )
    assert resp.status_code == 401


def test_login_unknown_user(client):
    resp = client.post(
        "/api/login",
        json={"correo": "nobody@example.com", "contrasena": "whatever"},
    )
    assert resp.status_code == 404


def test_authenticated_profile(client, app):
    with app.app_context():
        seed_user()
    login_resp = client.post(
        "/api/login",
        json={"correo": "user@example.com", "contrasena": "secret123"},
    )
    token = login_resp.get_json()["token"]
    resp = client.get("/api/perfil", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
