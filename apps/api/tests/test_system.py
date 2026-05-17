from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app

client = TestClient(app)
settings = get_settings()


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "guia-produto-radar-api",
        "environment": settings.app_env,
    }


def test_version() -> None:
    response = client.get("/version")

    assert response.status_code == 200
    data = response.json()
    assert data["project"] == "Guia Produto Radar"
    assert data["service"] == "guia-produto-radar-api"
    assert data["environment"] == settings.app_env
    assert data["version"] == "0.1.0"


def test_admin_cors_allows_configured_origin() -> None:
    origin = settings.admin_cors_origin_list[0]
    response = client.options(
        "/health",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == origin
