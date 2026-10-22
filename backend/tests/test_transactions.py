import io

def test_list_transactions(client):
    """Test getting paginated transactions."""
    response = client.get("/api/transactions")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert isinstance(data["items"], list)
    assert data["total"] > 0


def test_create_and_delete_transaction(client):
    """Test creating a transaction and deleting it."""
    payload = {
        "date": "2026-07-25",
        "type": "expense",
        "category": "Office Supplies",
        "amount": 1450.0,
        "tax_amount": 261.0,
        "vendor": "Stationery Mart",
        "description": "Billing paper and register books",
        "source": "manual",
    }
    create_res = client.post("/api/transactions", json=payload)
    assert create_res.status_code == 200
    created = create_res.json()
    assert created["id"] > 0
    assert created["amount"] == 1450.0

    # Delete
    del_res = client.delete(f"/api/transactions/{created['id']}")
    assert del_res.status_code == 200


def test_export_csv(client):
    """Test exporting transactions as CSV."""
    response = client.get("/api/transactions/export")
    assert response.status_code == 200
    assert "text/csv" in response.headers.get("content-type", "")
    content = response.text
    assert "date,type,category,amount" in content


def test_import_csv(client):
    """Test CSV batch import."""
    csv_content = (
        "date,type,category,amount,tax_amount,description,vendor\n"
        "2026-07-10,expense,Miscellaneous,500,0,Tea and refreshments,Sharma Tea\n"
        "2026-07-11,revenue,Product Sales,3200,576,Cash counter sales,Walk-in\n"
    )
    files = {"file": ("test_import.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")}
    response = client.post("/api/transactions/import", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data.get("imported_count") == 2
