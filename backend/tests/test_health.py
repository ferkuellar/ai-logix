def test_healthcheck_returns_ok(anonymous_client):
    response = anonymous_client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "ai-logix-backend"
