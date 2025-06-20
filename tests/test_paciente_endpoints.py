from datetime import datetime
from backend.app.config import db
from backend.app.models.paciente import Paciente
from backend.app.models.sms import Especialidad


def get_token(client, seed_user):
    resp = client.post(
        "/api/v1/auth/login",
        json={"correo": "user@example.com", "contrasena": "secret123"},
    )
    return resp.get_json()["token"]


def seed_data():
    esp = Especialidad(nombre="Dermatologia")
    db.session.add(esp)
    paciente = Paciente(nombre="Juan", celular="111", especialidad=esp,
                        programada=datetime.now())
    db.session.add(paciente)
    db.session.commit()
    return paciente


def test_listar_pacientes_returns_especialidad(client, app, seed_user):
    token = get_token(client, seed_user)
    with app.app_context():
        seed_data()
    resp = client.get("/api/pacientes", headers={"Authorization": token})
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["especialidad"] == "Dermatologia"
