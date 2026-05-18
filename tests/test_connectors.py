from __future__ import annotations

from packages.connectors import (
    AmazonCreatorsCredentials,
    BaseConnector,
    ConnectorConfig,
    ConnectorRequest,
    ConnectorRuntimeError,
    DataSourceManager,
    InMemoryRateLimiter,
    MockGoogleTrendsConnector,
    MockInternalDataConnector,
    build_default_mock_connectors,
    load_amazon_creators_credentials,
    load_connector_config,
)
from packages.connectors.models import NormalizedRecord


def test_all_default_mock_connectors_return_normalized_records() -> None:
    request = ConnectorRequest(
        query="melhor fone bluetooth",
        category="audio",
        product_slug="fone-bluetooth-demo",
        product_name="Fone Bluetooth Demo",
    )

    responses = [connector.fetch(request) for connector in build_default_mock_connectors()]

    assert len(responses) == 8
    assert all(response.ok for response in responses)
    assert all(response.records for response in responses)

    records = [record for response in responses for record in response.records]
    assert all(isinstance(record, NormalizedRecord) for record in records)
    assert {record.source for record in records} == {
        "google_trends",
        "google_ads_keyword_planner",
        "google_search_console",
        "amazon_creators",
        "mercado_livre",
        "shopee",
        "serp_api",
        "internal_data",
    }
    assert all(record.subject for record in records)
    assert all(0 <= record.confidence <= 1 for record in records)


def test_connector_config_is_loaded_from_environment(monkeypatch) -> None:
    monkeypatch.setenv("GPR_CONNECTOR_SERP_API_ENABLED", "false")
    monkeypatch.setenv("GPR_CONNECTOR_SERP_API_RATE_LIMIT_PER_MINUTE", "3")
    monkeypatch.setenv("GPR_CONNECTOR_SERP_API_TIMEOUT_SECONDS", "1.5")

    config = load_connector_config("serp_api")

    assert config.enabled is False
    assert config.rate_limit_per_minute == 3
    assert config.timeout_seconds == 1.5


def test_amazon_creators_credentials_are_loaded_without_leaking_secret(monkeypatch) -> None:
    monkeypatch.setenv("AMAZON_CREDENTIAL_ID", "credential-id-demo")
    monkeypatch.setenv("AMAZON_CREDENTIAL_SECRET", "credential-secret-demo")
    monkeypatch.setenv("AMAZON_CREATORS_VERSION", "2.1")

    credentials = load_amazon_creators_credentials()
    response = build_default_mock_connectors()[3].fetch(ConnectorRequest(query="echo dot"))
    record = response.records[0]

    assert isinstance(credentials, AmazonCreatorsCredentials)
    assert credentials.is_configured is True
    assert credentials.version == "2.1"
    assert record.attributes["credentials_configured"] is True
    assert record.attributes["api_version"] == "2.1"
    assert "credential-secret-demo" not in str(record)


def test_rate_limit_returns_controlled_error() -> None:
    connector = MockGoogleTrendsConnector(
        config=ConnectorConfig(source="google_trends", rate_limit_per_minute=1),
        rate_limiter=InMemoryRateLimiter(clock=lambda: 100.0),
    )
    request = ConnectorRequest(query="notebook gamer")

    first_response = connector.fetch(request)
    second_response = connector.fetch(request)

    assert first_response.ok is True
    assert second_response.ok is False
    assert second_response.rate_limited is True
    assert second_response.errors[0].code == "rate_limited"


def test_disabled_connector_does_not_fetch_data() -> None:
    connector = MockGoogleTrendsConnector(
        config=ConnectorConfig(source="google_trends", enabled=False)
    )

    response = connector.fetch(ConnectorRequest(query="smartwatch"))

    assert response.ok is False
    assert response.records == []
    assert response.errors[0].code == "connector_disabled"


class BrokenMockConnector(BaseConnector):
    source = "internal_data"

    def _fetch(self, request: ConnectorRequest) -> list[NormalizedRecord]:
        raise ConnectorRuntimeError(
            code="mock_failure",
            message="Falha simulada para teste.",
            retryable=False,
        )


def test_manager_does_not_stop_when_one_source_fails() -> None:
    manager = DataSourceManager(
        connectors=[
            BrokenMockConnector(),
            MockInternalDataConnector(),
        ]
    )

    responses = manager.collect(ConnectorRequest(query="tablet custo beneficio"))

    assert len(responses) == 2
    assert responses[0].ok is False
    assert responses[0].errors[0].code == "mock_failure"
    assert responses[1].ok is True
    assert responses[1].records
