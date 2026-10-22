def test_assistant_metric_query(client):
    """Test assistant answers metric questions."""
    payload = {
        "question": "How much was our revenue in July 2026?",
        "language": "en",
    }
    response = client.post("/api/assistant/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "metric" in data.get("agents_used", [])


def test_assistant_budget_query(client):
    """Test assistant answers budget questions."""
    payload = {
        "question": "Am I over budget in any category this month?",
        "language": "en",
    }
    response = client.post("/api/assistant/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "budget" in data.get("agents_used", [])


def test_assistant_compliance_query(client):
    """Test assistant routes compliance questions with citations and CA review flag."""
    payload = {
        "question": "What are the GST rules for small retailers?",
        "language": "en",
    }
    response = client.post("/api/assistant/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "compliance" in data.get("agents_used", [])
    assert len(data.get("sources", [])) > 0
    assert data.get("needs_ca_review") is True


def test_assistant_history(client):
    """Test query history endpoint returns past queries."""
    response = client.get("/api/assistant/history")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
