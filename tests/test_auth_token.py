from backend.app.config import db
from backend.app.models.user import Usuario, Rol


def seed_user():
    admin_role = Rol(id=1, nombre="Administrador")
    db.session.add(admin_role)
    user = Usuario(correo="admin@example.com", rol_id=1)
    user.set_contrasena("secret")
    db.session.add(user)
    db.session.commit()


def test_login_and_profile(client, app):
    with app.app_context():
        seed_user()
    # Login to obtain JWT token
    resp = client.post(
        "/api/login",
        json={"correo": "admin@example.com", "contrasena": "secret"},
    )
    assert resp.status_code == 200
    token = resp.get_json()["token"]

    # Access protected endpoint using raw token header
    resp2 = client.get("/api/perfil", headers={"Authorization": token})
    assert resp2.status_code == 200
    data = resp2.get_json()
    assert data["correo"] == "admin@example.com"
