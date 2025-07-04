def test_login_success(client, seed_user):
    resp = client.post(
        "/api/v1/auth/login",
        json={"correo": "user@example.com", "contrasena": "secret123"},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
    assert "token" in data
    assert data["rol"] == "Administrador"


def test_login_invalid_password(client, seed_user):
    resp = client.post(
        "/api/v1/auth/login",
        json={"correo": "user@example.com", "contrasena": "wrong"},
    )
    assert resp.status_code == 401


def test_login_unknown_user(client):
    resp = client.post(
        "/api/v1/auth/login",
        json={"correo": "nobody@example.com", "contrasena": "whatever"},
    )
    assert resp.status_code == 404


def test_authenticated_me(client, seed_user):
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"correo": "user@example.com", "contrasena": "secret123"},
    )
    token = login_resp.get_json()["token"]
    resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200


def test_register_returns_token(client, seed_user):
    resp = client.post(
        "/api/v1/auth/register",
        json={"correo": "new@example.com", "contrasena": "newpass"},
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["success"] is True
    assert "token" in data
