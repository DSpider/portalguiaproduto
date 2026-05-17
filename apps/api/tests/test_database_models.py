from decimal import Decimal

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from app.db.base import Base
from app.models import (
    AIContentDraft,
    Keyword,
    MarketplaceOffer,
    Product,
    ProductSource,
    ScoringRun,
    SeoPage,
    TrendSnapshot,
)


@pytest.fixture
def db_session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    testing_session = sessionmaker(bind=engine)
    session = testing_session()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
        engine.dispose()


def test_create_and_query_initial_schema_entities(db_session: Session) -> None:
    product = Product(
        name="Produto Demo",
        slug="produto-demo",
        brand="Marca Demo",
        category="notebooks",
        description="Produto ficticio para teste.",
        status="draft",
    )
    keyword = Keyword(
        keyword="notebook demo",
        category="notebooks",
        intent="comparativo",
        status="active",
    )
    seo_page = SeoPage(
        page_type="ranking",
        title="Ranking Demo",
        slug="ranking-demo",
        meta_description="Meta ficticia.",
        h1="Ranking Demo",
        status="draft",
    )

    db_session.add_all([product, keyword, seo_page])
    db_session.flush()

    db_session.add_all(
        [
            ProductSource(
                product_id=product.id,
                source_name="mock",
                source_url="https://example.test/produto",
                external_id="source-001",
                source_confidence=Decimal("0.90"),
            ),
            TrendSnapshot(
                product_id=product.id,
                keyword_id=keyword.id,
                source_name="mock",
                trend_score=Decimal("80.00"),
                search_interest=Decimal("70.00"),
                raw_payload={"mock": True},
            ),
            MarketplaceOffer(
                product_id=product.id,
                marketplace="mock_marketplace",
                external_id="offer-001",
                title="Oferta Demo",
                price=Decimal("1999.90"),
                currency="BRL",
                availability="in_stock",
            ),
            ScoringRun(
                product_id=product.id,
                score_total=Decimal("75.00"),
                score_trend=Decimal("80.00"),
                score_seo=Decimal("70.00"),
                score_commercial=Decimal("65.00"),
                score_confidence=Decimal("90.00"),
            ),
            AIContentDraft(
                seo_page_id=seo_page.id,
                product_id=product.id,
                draft_type="summary",
                content_json={"title": "Rascunho demo"},
                confidence_level="mock",
                review_status="pending",
            ),
        ]
    )
    db_session.commit()

    product_by_slug = db_session.scalar(select(Product).where(Product.slug == "produto-demo"))
    offer_by_marketplace = db_session.scalar(
        select(MarketplaceOffer).where(MarketplaceOffer.marketplace == "mock_marketplace")
    )
    draft_by_status = db_session.scalar(
        select(AIContentDraft).where(AIContentDraft.review_status == "pending")
    )

    assert product_by_slug is not None
    assert product_by_slug.category == "notebooks"
    assert offer_by_marketplace is not None
    assert offer_by_marketplace.external_id == "offer-001"
    assert draft_by_status is not None
    assert draft_by_status.content_json["title"] == "Rascunho demo"


def test_product_slug_must_be_unique(db_session: Session) -> None:
    db_session.add_all(
        [
            Product(name="Produto A", slug="produto-unico", category="audio"),
            Product(name="Produto B", slug="produto-unico", category="audio"),
        ]
    )

    with pytest.raises(IntegrityError):
        db_session.commit()


def test_offer_marketplace_external_id_must_be_unique(db_session: Session) -> None:
    product = Product(name="Produto Demo", slug="produto-demo", category="audio")
    db_session.add(product)
    db_session.flush()

    db_session.add_all(
        [
            MarketplaceOffer(
                product_id=product.id,
                marketplace="mock_marketplace",
                external_id="offer-duplicada",
                title="Oferta A",
                currency="BRL",
            ),
            MarketplaceOffer(
                product_id=product.id,
                marketplace="mock_marketplace",
                external_id="offer-duplicada",
                title="Oferta B",
                currency="BRL",
            ),
        ]
    )

    with pytest.raises(IntegrityError):
        db_session.commit()
