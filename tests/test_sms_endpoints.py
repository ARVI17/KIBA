from datetime import datetime, timedelta
from backend.app.config import db
from backend.app.models.sms import SMS
from backend.app.models.user import Rol, Usuario


def seed_sms():
    now = datetime.now().replace(second=0, microsecond=0)
    yesterday = now - timedelta(days=1)
    msgs = [
        SMS(celular="111", mensaje="A", fecha_envio=now, estado="Entregado"),
        SMS(celular="222", mensaje="B", fecha_envio=now, estado="Entregado"),
        SMS(celular="333", mensaje="C", fecha_envio=now, estado="Fallido"),
        SMS(celular="444", mensaje="D", fecha_envio=yesterday, estado="Entregado"),
    ]
    db.session.add_all(msgs)
    db.session.commit()


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


def test_dashboard_counts(client, app):
    token = get_token(client, app)
    with app.app_context():
        seed_sms()
    resp = client.get("/api/dashboard", headers={"Authorization": token})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["enviados"] == 3
    assert data["entregados"] == 2
    assert data["fallidos"] == 1
    assert len(data["dias"]) == 7
    assert len(data["cantidades"]) == 7
    assert data["cantidades"][-1] == 3
    assert data["cantidades"][-2] == 1


def test_historial_response(client, app):
    token = get_token(client, app)
    with app.app_context():
        seed_sms()
    resp = client.get("/api/historial", headers={"Authorization": token})
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 4
    assert data[-1]["numero"] == "444"
    assert {"fecha_envio", "numero", "mensaje", "estado"} <= data[0].keys()


def test_dashboard_requires_token(client, app):
    with app.app_context():
        seed_sms()
    resp = client.get("/api/dashboard")
    assert resp.status_code == 401


def test_historial_requires_token(client, app):
    with app.app_context():
        seed_sms()
    resp = client.get("/api/historial")
    assert resp.status_code == 401


def test_enviar_sms_requires_token(client):
    resp = client.post("/api/enviar-sms", json={"numero": "1", "mensaje": "hi"})
    assert resp.status_code == 401


def test_importar_sms_requires_token(client):
    resp = client.post(
        "/api/importar-sms",
        json={"mensajes": [{"numero": "1", "mensaje": "hi"}]},
    )
    assert resp.status_code == 401


def test_enviar_sms_with_token(client, app, monkeypatch):
    token = get_token(client, app)

    def mock_post(url, headers=None, data=None):
        class R:
            status_code = 200
            text = ""

        return R()

    monkeypatch.setattr("backend.app.routes.sms.requests.post", mock_post)
    resp = client.post(
        "/api/enviar-sms",
        json={"numero": "1", "mensaje": "hi"},
        headers={"Authorization": token},
    )
    assert resp.status_code == 200


def test_importar_sms_with_token(client, app, monkeypatch):
    token = get_token(client, app)

    def mock_post(url, headers=None, data=None):
        class R:
            status_code = 200
            text = ""

        return R()

    monkeypatch.setattr("backend.app.routes.sms.requests.post", mock_post)
    resp = client.post(
        "/api/importar-sms",
        json={"mensajes": [{"numero": "1", "mensaje": "hi"}]},
        headers={"Authorization": token},
    )
    assert resp.status_code == 200
