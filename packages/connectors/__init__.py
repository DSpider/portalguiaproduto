"""Conectores de dados do Guia Produto Radar."""

from packages.connectors.base import BaseConnector
from packages.connectors.config import ConnectorConfig, load_connector_config
from packages.connectors.errors import ConnectorRuntimeError
from packages.connectors.manager import DataSourceManager
from packages.connectors.mock_sources import (
    MockAmazonCreatorsConnector,
    MockGoogleAdsKeywordPlannerConnector,
    MockGoogleSearchConsoleConnector,
    MockGoogleTrendsConnector,
    MockInternalDataConnector,
    MockMercadoLivreConnector,
    MockSerpApiConnector,
    MockShopeeConnector,
    build_default_mock_connectors,
)
from packages.connectors.models import (
    ConnectorError,
    ConnectorRequest,
    ConnectorResponse,
    ConnectorSource,
    NormalizedRecord,
    RecordType,
)
from packages.connectors.rate_limit import InMemoryRateLimiter

__all__ = [
    "BaseConnector",
    "ConnectorConfig",
    "ConnectorError",
    "ConnectorRequest",
    "ConnectorResponse",
    "ConnectorRuntimeError",
    "ConnectorSource",
    "DataSourceManager",
    "InMemoryRateLimiter",
    "MockAmazonCreatorsConnector",
    "MockGoogleAdsKeywordPlannerConnector",
    "MockGoogleSearchConsoleConnector",
    "MockGoogleTrendsConnector",
    "MockInternalDataConnector",
    "MockMercadoLivreConnector",
    "MockSerpApiConnector",
    "MockShopeeConnector",
    "NormalizedRecord",
    "RecordType",
    "build_default_mock_connectors",
    "load_connector_config",
]
