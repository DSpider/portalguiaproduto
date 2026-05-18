from __future__ import annotations

import os
from dataclasses import dataclass

from packages.connectors.models import ConnectorSource


@dataclass(frozen=True)
class ConnectorConfig:
    source: ConnectorSource
    enabled: bool = True
    rate_limit_per_minute: int = 60
    timeout_seconds: float = 5.0


@dataclass(frozen=True)
class AmazonCreatorsCredentials:
    credential_id: str | None = None
    credential_secret: str | None = None
    version: str = "2.1"

    @property
    def is_configured(self) -> bool:
        return bool(self.credential_id and self.credential_secret)


def _source_env_name(source: ConnectorSource) -> str:
    return source.upper()


def _get_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "on"}


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default

    try:
        return int(value)
    except ValueError:
        return default


def _get_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default

    try:
        return float(value)
    except ValueError:
        return default


def _get_optional_string(name: str) -> str | None:
    value = os.getenv(name)
    if value is None:
        return None

    value = value.strip()
    return value or None


def load_connector_config(source: ConnectorSource) -> ConnectorConfig:
    env_prefix = f"GPR_CONNECTOR_{_source_env_name(source)}"

    return ConnectorConfig(
        source=source,
        enabled=_get_bool(f"{env_prefix}_ENABLED", True),
        rate_limit_per_minute=max(0, _get_int(f"{env_prefix}_RATE_LIMIT_PER_MINUTE", 60)),
        timeout_seconds=max(0.1, _get_float(f"{env_prefix}_TIMEOUT_SECONDS", 5.0)),
    )


def load_amazon_creators_credentials() -> AmazonCreatorsCredentials:
    return AmazonCreatorsCredentials(
        credential_id=_get_optional_string("AMAZON_CREDENTIAL_ID"),
        credential_secret=_get_optional_string("AMAZON_CREDENTIAL_SECRET"),
        version=os.getenv("AMAZON_CREATORS_VERSION", "2.1").strip() or "2.1",
    )
