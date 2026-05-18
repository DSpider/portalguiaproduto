from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import create_app


@pytest.fixture(autouse=True)
def clear_settings_cache() -> Iterator[None]:
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def make_client(
    monkeypatch: pytest.MonkeyPatch,
    *,
    auth_enabled: bool,
    token: str | None = "admin-token-for-tests-123456",
) -> TestClient:
    monkeypatch.setenv("ADMIN_AUTH_ENABLED", "true" if auth_enabled else "false")
    if token is None:
        monkeypatch.delenv("ADMIN_API_TOKEN", raising=False)
    else:
        monkeypatch.setenv("ADMIN_API_TOKEN", token)

    get_settings.cache_clear()
    return TestClient(create_app())


def test_admin_status_allows_request_when_auth_is_disabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = make_client(monkeypatch, auth_enabled=False, token=None)

    response = client.get("/api/v1/admin/status")

    assert response.status_code == 200
    data = response.json()
    assert data["auth_enabled"] is False
    assert data["auth_mode"] == "admin_token"


def test_admin_status_rejects_missing_token_when_auth_is_enabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = make_client(monkeypatch, auth_enabled=True)

    response = client.get("/api/v1/admin/status")

    assert response.status_code == 401


def test_admin_status_rejects_invalid_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = make_client(monkeypatch, auth_enabled=True)

    response = client.get(
        "/api/v1/admin/status",
        headers={"Authorization": "Bearer wrong-token"},
    )

    assert response.status_code == 401


def test_admin_status_accepts_bearer_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    token = "admin-token-for-tests-123456"
    client = make_client(monkeypatch, auth_enabled=True, token=token)

    response = client.get(
        "/api/v1/admin/status",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["auth_enabled"] is True


def test_admin_status_accepts_custom_header_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    token = "admin-token-for-tests-123456"
    client = make_client(monkeypatch, auth_enabled=True, token=token)

    response = client.get(
        "/api/v1/admin/status",
        headers={"X-GPR-Admin-Token": token},
    )

    assert response.status_code == 200


def test_admin_status_fails_when_auth_is_enabled_without_configured_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = make_client(monkeypatch, auth_enabled=True, token=None)

    response = client.get("/api/v1/admin/status")

    assert response.status_code == 503


def test_content_briefing_requires_admin_token_when_auth_is_enabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = make_client(monkeypatch, auth_enabled=True)
    payload = {
        "produto": {
            "name": "Produto Demo",
            "description": "Produto ficticio para teste.",
        },
        "categoria": "tecnologia",
        "palavra_chave_principal": "produto demo",
        "palavras_chave_secundarias": [],
        "tendencia": {"source_name": "mock"},
        "ofertas_disponiveis": [],
        "dados_de_avaliacao": {"source_is_reliable": False},
        "concorrentes": [],
        "score_calculado": {"score_total": 50, "score_confidence": 50},
    }

    response = client.post("/api/v1/content/briefing", json=payload)

    assert response.status_code == 401
