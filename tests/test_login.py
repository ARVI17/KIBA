def test_login_campos_faltantes(client):
    res = client.post("/api/login", json={})
    assert res.status_code == 400
