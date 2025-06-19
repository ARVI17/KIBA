from datetime import datetime
from backend.app.config import db
from backend.app.models.sms import SMS, Especialidad
from backend.app.models.paciente import Paciente
from backend.app.models.cita import Cita


def get_token(client, seed_user):
    resp = client.post(
        "/api/login",
        json={"correo": "user@example.com", "contrasena": "secret123"},
    )
    return resp.get_json()["token"]


def seed_data():
    esp = Especialidad(nombre="General")
    db.session.add(esp)
    paciente = Paciente(nombre="Ana", celular="123", especialidad=esp)
    db.session.add(paciente)
    fecha = datetime.now().replace(microsecond=0)
    cita = Cita(paciente=paciente, especialidad=esp, fecha_hora=fecha)
    sms = SMS(celular="123", mensaje="hola", especialidad=esp, fecha_envio=fecha)
    db.session.add_all([cita, sms])
    db.session.commit()
    return paciente, cita, sms


def test_confirmar_cita_creates_confirmation(client, app, seed_user):
    token = get_token(client, seed_user)
    with app.app_context():
        paciente, cita, sms = seed_data()
    resp = client.post(
        "/api/confirmar-cita",
        headers={"Authorization": token},
        json={"celular": "123", "fecha_hora": cita.fecha_hora.strftime("%Y-%m-%d %H:%M:%S")},
    )
    assert resp.status_code == 200
    with app.app_context():
        conf = cita.confirmaciones[0]
        assert conf.sms_id == sms.id


def test_crear_cita_fecha_invalida(client, app, seed_user):
    token = get_token(client, seed_user)
    with app.app_context():
        esp = Especialidad(nombre="General")
        db.session.add(esp)
        paciente = Paciente(nombre="Ana", celular="555", especialidad=esp)
        db.session.add(paciente)
        db.session.commit()
        esp_id = esp.id

    resp = client.post(
        "/api/citas",
        headers={"Authorization": token},
        json={"celular": "555", "especialidad_id": esp_id, "fecha_hora": "bad"},
    )
    assert resp.status_code == 400


def test_crear_paciente_programada_invalida(client, app, seed_user):
    token = get_token(client, seed_user)
    with app.app_context():
        esp = Especialidad(nombre="General")
        db.session.add(esp)
        db.session.commit()
        esp_id = esp.id

    resp = client.post(
        "/api/pacientes",
        headers={"Authorization": token},
        json={
            "nombre": "Ana",
            "celular": "777",
            "especialidad_id": esp_id,
            "programada": "not-a-date",
        },
    )
    assert resp.status_code == 400
