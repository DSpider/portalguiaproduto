from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Literal


ConnectorSource = Literal[
    "google_trends",
    "google_ads_keyword_planner",
    "google_search_console",
    "amazon_creators",
    "mercado_livre",
    "shopee",
    "serp_api",
    "internal_data",
]

RecordType = Literal[
    "trend",
    "keyword",
    "search_console",
    "offer",
    "serp",
    "internal_product",
]


@dataclass(frozen=True)
class ConnectorRequest:
    query: str
    category: str | None = None
    product_slug: str | None = None
    product_name: str | None = None
    country: str = "BR"
    locale: str = "pt-BR"
    limit: int = 10


@dataclass(frozen=True)
class NormalizedRecord:
    source: ConnectorSource
    record_type: RecordType
    subject: str
    title: str | None = None
    url: str | None = None
    external_id: str | None = None
    metrics: dict[str, Any] = field(default_factory=dict)
    attributes: dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    observed_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    raw_payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ConnectorError:
    source: ConnectorSource
    code: str
    message: str
    retryable: bool = True


@dataclass(frozen=True)
class ConnectorResponse:
    source: ConnectorSource
    ok: bool
    records: list[NormalizedRecord] = field(default_factory=list)
    errors: list[ConnectorError] = field(default_factory=list)
    rate_limited: bool = False
    duration_ms: float = 0.0
