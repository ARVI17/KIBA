def get_token(client, seed_user):
    resp = client.post(
        "/api/v1/auth/login",
        json={"correo": "user@example.com", "contrasena": "secret123"},
    )
    return resp.get_json()["token"]


def test_confirmaciones_requires_token(client):
    resp = client.get("/api/confirmaciones")
    assert resp.status_code == 401


def test_confirmaciones_with_token(client, seed_user):
    token = get_token(client, seed_user)
    resp = client.get("/api/confirmaciones", headers={"Authorization": token})
    assert resp.status_code == 200


from datetime import datetime
from backend.app.config import db
from backend.app.models.sms import SMS, Especialidad
from backend.app.models.paciente import Paciente
from backend.app.models.cita import Cita
from backend.app.models.confirmacion import Confirmacion


def seed_conf_data():
    fecha = datetime.now().replace(microsecond=0)
    esp = Especialidad(nombre="General")
    db.session.add(esp)
    paciente = Paciente(nombre="Ana", celular="123", especialidad=esp)
    cita = Cita(paciente=paciente, especialidad=esp, fecha_hora=fecha)
    sms = SMS(celular="123", mensaje="hola", especialidad=esp, fecha_envio=fecha)
    conf = Confirmacion(cita=cita, sms=sms, confirmada_en=fecha)
    db.session.add_all([paciente, cita, sms, conf])
    db.session.commit()
    return fecha.date(), paciente.id


def test_confirmaciones_filtering(client, app, seed_user):
    token = get_token(client, seed_user)
    with app.app_context():
        fecha, pid = seed_conf_data()
    resp = client.get(
        f"/api/confirmaciones?fecha={fecha}&paciente_id={pid}",
        headers={"Authorization": token},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["paciente"]["id"] == pid
