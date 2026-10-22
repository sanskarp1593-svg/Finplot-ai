def test_health_check(client):
    """Test health endpoint returns status healthy or ok."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] in ("healthy", "ok")
