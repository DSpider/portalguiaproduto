from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Importa os modelos para que o Alembic enxergue o metadata completo.
from app.models.ai_content_draft import AIContentDraft  # noqa: E402,F401
from app.models.keyword import Keyword  # noqa: E402,F401
from app.models.marketplace_offer import MarketplaceOffer  # noqa: E402,F401
from app.models.product import Product  # noqa: E402,F401
from app.models.product_source import ProductSource  # noqa: E402,F401
from app.models.scoring_run import ScoringRun  # noqa: E402,F401
from app.models.seo_page import SeoPage  # noqa: E402,F401
from app.models.trend_snapshot import TrendSnapshot  # noqa: E402,F401
