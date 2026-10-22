def test_dashboard_metrics(client):
    """Test dashboard calculations for a specific month."""
    response = client.get("/api/dashboard?month=2026-07")
    assert response.status_code == 200
    data = response.json()

    assert "summary" in data
    assert "change" in data
    assert "category_breakdown" in data
    assert "budget_progress" in data

    summary = data["summary"]
    assert "revenue" in summary
    assert "expenses" in summary
    assert "profit" in summary
    assert "margin" in summary

    # Sanity checks
    assert summary["revenue"] >= 0
    assert summary["expenses"] >= 0
    assert round(summary["revenue"] - summary["expenses"], 2) == round(summary["profit"], 2)
    assert isinstance(data["category_breakdown"], list)
    assert len(data["category_breakdown"]) > 0
    assert isinstance(data["budget_progress"], list)
