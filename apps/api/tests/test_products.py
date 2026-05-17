from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_products() -> None:
    response = client.get("/api/v1/products")

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["slug"] == "notebook-ultrafino-14"
    assert "summary" not in data[0]


def test_get_product_by_slug() -> None:
    response = client.get("/api/v1/products/notebook-ultrafino-14")

    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == "notebook-ultrafino-14"
    assert data["confidence"] == "mock"
    assert data["data_sources"] == ["mock"]


def test_get_product_by_unknown_slug_returns_404() -> None:
    response = client.get("/api/v1/products/produto-inexistente")

    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "not_found"
