def get_token(client, seed_user):
    resp = client.post(
        "/api/login",
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
