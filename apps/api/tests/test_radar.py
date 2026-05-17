from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_radar_summary() -> None:
    response = client.get("/api/v1/radar/summary")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["mode"] == "mock"
    assert data["total_products"] >= 1
    assert "notebooks" in data["top_categories"]
    assert len(data["highlighted_products"]) >= 1
