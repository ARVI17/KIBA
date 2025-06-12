from datetime import datetime, timedelta
from unittest.mock import patch
from backend.app.config import db
from backend.app.models.sms import SMS


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


def test_dashboard_counts(client, app, auth_headers):
    with app.app_context():
        seed_sms()
    resp = client.get("/api/dashboard", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["enviados"] == 3
    assert data["entregados"] == 2
    assert data["fallidos"] == 1
    assert len(data["dias"]) == 7
    assert len(data["cantidades"]) == 7
    assert data["cantidades"][-1] == 3
    assert data["cantidades"][-2] == 1


def test_historial_response(client, app, auth_headers):
    with app.app_context():
        seed_sms()
    resp = client.get("/api/historial", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 4
    assert data[-1]["numero"] == "444"
    assert {"fecha_envio", "numero", "mensaje", "estado"} <= data[0].keys()


def test_dashboard_requires_token(client):
    resp = client.get("/api/dashboard")
    assert resp.status_code == 401


def test_historial_requires_token(client):
    resp = client.get("/api/historial")
    assert resp.status_code == 401


def test_enviar_sms_requires_token(client):
    resp = client.post("/api/enviar-sms", json={"numero": "1", "mensaje": "hi"})
    assert resp.status_code == 401


def test_importar_sms_requires_token(client):
    resp = client.post("/api/importar-sms", json={"mensajes": []})
    assert resp.status_code == 401


def test_enviar_sms_success(client, auth_headers):
    with patch("backend.app.routes.sms.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        resp = client.post(
            "/api/enviar-sms",
            json={"numero": "123", "mensaje": "hola"},
            headers=auth_headers,
        )
        assert resp.status_code == 200


def test_importar_sms_success(client, auth_headers):
    with patch("backend.app.routes.sms.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        resp = client.post(
            "/api/importar-sms",
            json={"mensajes": [{"numero": "1", "mensaje": "a"}]},
            headers=auth_headers,
        )
        assert resp.status_code == 200
