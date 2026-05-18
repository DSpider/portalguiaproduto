from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from packages.connectors.base import BaseConnector
from packages.connectors.models import ConnectorRequest, NormalizedRecord


def _subject(request: ConnectorRequest) -> str:
    return request.product_name or request.query


def _observed_at() -> datetime:
    return datetime(2026, 5, 17, 12, 0, tzinfo=UTC)


class MockGoogleTrendsConnector(BaseConnector):
    source = "google_trends"

    def _fetch(self, request: ConnectorRequest) -> list[NormalizedRecord]:
        return [
            NormalizedRecord(
                source=self.source,
                record_type="trend",
                subject=_subject(request),
                metrics={
                    "trend_growth_percent": 38.0,
                    "search_interest": 74,
                    "period_days": 30,
                },
                attributes={
                    "country": request.country,
                    "locale": request.locale,
                    "category": request.category,
                },
                confidence=0.72,
                observed_at=_observed_at(),
                raw_payload={"mock": True, "source_note": "google_trends_mock"},
            )
        ]


class MockGoogleAdsKeywordPlannerConnector(BaseConnector):
    source = "google_ads_keyword_planner"

    def _fetch(self, request: ConnectorRequest) -> list[NormalizedRecord]:
        return [
            NormalizedRecord(
                source=self.source,
                record_type="keyword",
                subject=request.query,
                metrics={
                    "estimated_search_volume": 5400,
                    "competition_index": 0.61,
                    "suggested_bid_brl": 1.95,
                },
                attributes={
                    "intent": "comparativo",
                    "country": request.country,
                    "locale": request.locale,
                },
                confidence=0.70,
                observed_at=_observed_at(),
                raw_payload={"mock": True, "source_note": "keyword_planner_mock"},
            )
        ]


class MockGoogleSearchConsoleConnector(BaseConnector):
    source = "google_search_console"

    def _fetch(self, request: ConnectorRequest) -> list[NormalizedRecord]:
        url = f"https://www.guiaproduto.com.br/{request.product_slug or 'radar-teste'}/"

        return [
            NormalizedRecord(
                source=self.source,
                record_type="search_console",
                subject=request.query,
                title="Pagina Guia Produto monitorada",
                url=url,
                metrics={
                    "clicks": 120,
                    "impressions": 4800,
                    "ctr": 0.025,
                    "average_position": 12.4,
                },
                attributes={"query": request.query, "page": url},
                confidence=0.85,
                observed_at=_observed_at(),
                raw_payload={"mock": True, "source_note": "search_console_mock"},
            )
        ]


class MockAmazonCreatorsConnector(BaseConnector):
    source = "amazon_creators"

    def _fetch(self, request: ConnectorRequest) -> list[NormalizedRecord]:
        return [
            NormalizedRecord(
                source=self.source,
                record_type="offer",
                subject=_subject(request),
                title=f"{_subject(request)} - Oferta Amazon Demo",
                url="https://example.test/amazon/oferta-demo",
                external_id="amazon-demo-001",
                metrics={
                    "price": Decimal("499.90"),
                    "old_price": Decimal("549.90"),
                    "rating": 4.6,
                    "reviews_count": 320,
                    "commission_rate_percent": 4.0,
                },
                attributes={
                    "marketplace": "amazon",
                    "currency": "BRL",
                    "availability": "in_stock",
                },
                confidence=0.68,
                observed_at=_observed_at(),
                raw_payload={"mock": True, "source_note": "amazon_creators_mock"},
            )
        ]


class MockMercadoLivreConnector(BaseConnector):
    source = "mercado_livre"

    def _fetch(self, request: ConnectorRequest) -> list[NormalizedRecord]:
        return [
            NormalizedRecord(
                source=self.source,
                record_type="offer",
                subject=_subject(request),
                title=f"{_subject(request)} - Oferta Mercado Livre Demo",
                url="https://example.test/mercado-livre/oferta-demo",
                external_id="ml-demo-001",
                metrics={
                    "price": Decimal("489.90"),
                    "old_price": None,
                    "rating": 4.7,
                    "reviews_count": 210,
                    "commission_rate_percent": 3.5,
                },
                attributes={
                    "marketplace": "mercado_livre",
                    "currency": "BRL",
                    "availability": "in_stock",
                },
                confidence=0.66,
                observed_at=_observed_at(),
                raw_payload={"mock": True, "source_note": "mercado_livre_mock"},
            )
        ]


class MockShopeeConnector(BaseConnector):
    source = "shopee"

    def _fetch(self, request: ConnectorRequest) -> list[NormalizedRecord]:
        return [
            NormalizedRecord(
                source=self.source,
                record_type="offer",
                subject=_subject(request),
                title=f"{_subject(request)} - Oferta Shopee Demo",
                url="https://example.test/shopee/oferta-demo",
                external_id="shopee-demo-001",
                metrics={
                    "price": Decimal("459.90"),
                    "old_price": Decimal("519.90"),
                    "rating": 4.5,
                    "reviews_count": 88,
                    "commission_rate_percent": 5.0,
                },
                attributes={
                    "marketplace": "shopee",
                    "currency": "BRL",
                    "availability": "in_stock",
                },
                confidence=0.62,
                observed_at=_observed_at(),
                raw_payload={"mock": True, "source_note": "shopee_mock"},
            )
        ]


class MockSerpApiConnector(BaseConnector):
    source = "serp_api"

    def _fetch(self, request: ConnectorRequest) -> list[NormalizedRecord]:
        return [
            NormalizedRecord(
                source=self.source,
                record_type="serp",
                subject=request.query,
                title="SERP demo para oportunidade SEO",
                url="https://example.test/serp/demo",
                metrics={
                    "seo_competition": 0.58,
                    "ads_count": 3,
                    "organic_results_count": 10,
                    "featured_snippet_present": False,
                },
                attributes={
                    "country": request.country,
                    "locale": request.locale,
                    "top_domains": ["example.test", "concorrente.test"],
                },
                confidence=0.64,
                observed_at=_observed_at(),
                raw_payload={"mock": True, "source_note": "serp_api_mock"},
            )
        ]


class MockInternalDataConnector(BaseConnector):
    source = "internal_data"

    def _fetch(self, request: ConnectorRequest) -> list[NormalizedRecord]:
        slug = request.product_slug or "produto-demo"

        return [
            NormalizedRecord(
                source=self.source,
                record_type="internal_product",
                subject=_subject(request),
                title=request.product_name or "Produto Demo Guia Produto",
                url=f"https://www.guiaproduto.com.br/{slug}/",
                external_id=slug,
                metrics={
                    "editorial_priority": 0.8,
                    "existing_page": bool(request.product_slug),
                    "internal_score": 76,
                },
                attributes={
                    "category": request.category,
                    "status": "draft",
                    "review_required": True,
                },
                confidence=0.90,
                observed_at=_observed_at(),
                raw_payload={"mock": True, "source_note": "internal_data_mock"},
            )
        ]


def build_default_mock_connectors() -> list[BaseConnector]:
    return [
        MockGoogleTrendsConnector(),
        MockGoogleAdsKeywordPlannerConnector(),
        MockGoogleSearchConsoleConnector(),
        MockAmazonCreatorsConnector(),
        MockMercadoLivreConnector(),
        MockShopeeConnector(),
        MockSerpApiConnector(),
        MockInternalDataConnector(),
    ]
