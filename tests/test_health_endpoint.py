def test_db_health(client):
    resp = client.get('/api/v1/health/db')
    assert resp.status_code == 200
    assert resp.get_json() == {'status': 'ok'}
