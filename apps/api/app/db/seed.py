from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import select

from app.db.session import SessionLocal
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


def seed_database() -> None:
    with SessionLocal() as session:
        product = session.scalar(
            select(Product).where(Product.slug == "notebook-ultrafino-14-demo")
        )
        if product is None:
            product = Product(
                name="Notebook Ultrafino 14 Demo",
                slug="notebook-ultrafino-14-demo",
                brand="Marca Demo",
                category="notebooks",
                description="Produto ficticio usado apenas para validar o schema inicial.",
                image_url=None,
                status="draft",
            )
            session.add(product)
            session.flush()

        keyword = session.scalar(
            select(Keyword).where(Keyword.keyword == "notebook leve para estudar demo")
        )
        if keyword is None:
            keyword = Keyword(
                keyword="notebook leve para estudar demo",
                category="notebooks",
                intent="comparativo",
                status="active",
            )
            session.add(keyword)
            session.flush()

        seo_page = session.scalar(
            select(SeoPage).where(SeoPage.slug == "melhores-notebooks-leves-demo")
        )
        if seo_page is None:
            seo_page = SeoPage(
                page_type="ranking",
                title="Melhores notebooks leves demo",
                slug="melhores-notebooks-leves-demo",
                meta_description="Pagina ficticia para validar o schema SEO.",
                h1="Melhores notebooks leves demo",
                status="draft",
                canonical_url=None,
            )
            session.add(seo_page)
            session.flush()

        if not product.sources:
            session.add(
                ProductSource(
                    product_id=product.id,
                    source_name="mock",
                    source_url="https://example.test/produto-demo",
                    external_id="mock-product-001",
                    source_confidence=Decimal("0.80"),
                    last_checked_at=datetime.now(timezone.utc),
                )
            )

        existing_offer = session.scalar(
            select(MarketplaceOffer).where(
                MarketplaceOffer.marketplace == "mock_marketplace",
                MarketplaceOffer.external_id == "mock-offer-001",
            )
        )
        if existing_offer is None:
            session.add(
                MarketplaceOffer(
                    product_id=product.id,
                    marketplace="mock_marketplace",
                    external_id="mock-offer-001",
                    title="Oferta ficticia de notebook demo",
                    price=Decimal("3999.90"),
                    old_price=Decimal("4299.90"),
                    currency="BRL",
                    affiliate_url="https://example.test/oferta-demo",
                    image_url=None,
                    rating=Decimal("4.50"),
                    reviews_count=12,
                    availability="in_stock",
                    last_checked_at=datetime.now(timezone.utc),
                )
            )

        session.add(
            TrendSnapshot(
                product_id=product.id,
                keyword_id=keyword.id,
                source_name="mock",
                trend_score=Decimal("78.50"),
                search_interest=Decimal("62.00"),
                period_start=datetime(2026, 5, 1, tzinfo=timezone.utc),
                period_end=datetime(2026, 5, 16, tzinfo=timezone.utc),
                raw_payload={"source": "mock", "note": "sem dados reais"},
            )
        )
        session.add(
            ScoringRun(
                product_id=product.id,
                score_total=Decimal("76.20"),
                score_trend=Decimal("78.50"),
                score_seo=Decimal("72.00"),
                score_commercial=Decimal("70.00"),
                score_confidence=Decimal("80.00"),
                explanation="Score ficticio para validar persistencia inicial.",
            )
        )

        existing_draft = session.scalar(
            select(AIContentDraft).where(
                AIContentDraft.seo_page_id == seo_page.id,
                AIContentDraft.product_id == product.id,
                AIContentDraft.draft_type == "ranking_intro",
            )
        )
        if existing_draft is None:
            session.add(
                AIContentDraft(
                    seo_page_id=seo_page.id,
                    product_id=product.id,
                    draft_type="ranking_intro",
                    content_json={
                        "title": "Rascunho ficticio",
                        "limitations": ["Dados mockados", "Requer revisao humana"],
                    },
                    confidence_level="mock",
                    review_status="pending",
                )
            )

        session.commit()


if __name__ == "__main__":
    seed_database()
    print("Seed mockado concluido com sucesso.")
