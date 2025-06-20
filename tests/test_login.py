def test_login_campos_faltantes(client):
    res = client.post("/api/v1/auth/login", json={})
    assert res.status_code == 400
