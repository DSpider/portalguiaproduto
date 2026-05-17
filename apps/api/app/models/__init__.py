"""Modelos SQLAlchemy do Guia Produto Radar."""

from app.models.ai_content_draft import AIContentDraft
from app.models.keyword import Keyword
from app.models.marketplace_offer import MarketplaceOffer
from app.models.product import Product
from app.models.product_source import ProductSource
from app.models.scoring_run import ScoringRun
from app.models.seo_page import SeoPage
from app.models.trend_snapshot import TrendSnapshot

__all__ = [
    "AIContentDraft",
    "Keyword",
    "MarketplaceOffer",
    "Product",
    "ProductSource",
    "ScoringRun",
    "SeoPage",
    "TrendSnapshot",
]
