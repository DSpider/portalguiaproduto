"""initial Guia Produto Radar schema

Revision ID: 20260516_0001
Revises:
Create Date: 2026-05-16
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260516_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("brand", sa.String(length=120), nullable=True),
        sa.Column("category", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("image_url", sa.String(length=2048), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_products_slug", "products", ["slug"], unique=True)
    op.create_index("ix_products_category", "products", ["category"])
    op.create_index("ix_products_status", "products", ["status"])
    op.create_index("ix_products_created_at", "products", ["created_at"])

    op.create_table(
        "keywords",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("keyword", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=120), nullable=False),
        sa.Column("intent", sa.String(length=80), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_keywords_keyword", "keywords", ["keyword"])
    op.create_index("ix_keywords_category", "keywords", ["category"])
    op.create_index("ix_keywords_status", "keywords", ["status"])
    op.create_index("ix_keywords_created_at", "keywords", ["created_at"])

    op.create_table(
        "seo_pages",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("page_type", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("meta_description", sa.String(length=320), nullable=True),
        sa.Column("h1", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("canonical_url", sa.String(length=2048), nullable=True),
        sa.Column("last_generated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_seo_pages_page_type", "seo_pages", ["page_type"])
    op.create_index("ix_seo_pages_slug", "seo_pages", ["slug"], unique=True)
    op.create_index("ix_seo_pages_status", "seo_pages", ["status"])
    op.create_index("ix_seo_pages_created_at", "seo_pages", ["created_at"])

    op.create_table(
        "product_sources",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("source_name", sa.String(length=120), nullable=False),
        sa.Column("source_url", sa.String(length=2048), nullable=True),
        sa.Column("external_id", sa.String(length=255), nullable=True),
        sa.Column("source_confidence", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("last_checked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_product_sources_product_id", "product_sources", ["product_id"])
    op.create_index("ix_product_sources_source_name", "product_sources", ["source_name"])
    op.create_index("ix_product_sources_created_at", "product_sources", ["created_at"])

    op.create_table(
        "trend_snapshots",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=True),
        sa.Column("keyword_id", sa.Integer(), nullable=True),
        sa.Column("source_name", sa.String(length=120), nullable=False),
        sa.Column("trend_score", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("search_interest", sa.Numeric(precision=6, scale=2), nullable=True),
        sa.Column("period_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("period_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("raw_payload", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["keyword_id"], ["keywords.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_trend_snapshots_product_id", "trend_snapshots", ["product_id"])
    op.create_index("ix_trend_snapshots_keyword_id", "trend_snapshots", ["keyword_id"])
    op.create_index("ix_trend_snapshots_source_name", "trend_snapshots", ["source_name"])
    op.create_index("ix_trend_snapshots_created_at", "trend_snapshots", ["created_at"])

    op.create_table(
        "marketplace_offers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("marketplace", sa.String(length=80), nullable=False),
        sa.Column("external_id", sa.String(length=255), nullable=True),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("price", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("old_price", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("affiliate_url", sa.String(length=2048), nullable=True),
        sa.Column("image_url", sa.String(length=2048), nullable=True),
        sa.Column("rating", sa.Numeric(precision=3, scale=2), nullable=True),
        sa.Column("reviews_count", sa.Integer(), nullable=True),
        sa.Column("availability", sa.String(length=80), nullable=True),
        sa.Column("last_checked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "marketplace",
            "external_id",
            name="uq_marketplace_offers_marketplace_external_id",
        ),
    )
    op.create_index("ix_marketplace_offers_product_id", "marketplace_offers", ["product_id"])
    op.create_index("ix_marketplace_offers_marketplace", "marketplace_offers", ["marketplace"])
    op.create_index("ix_marketplace_offers_availability", "marketplace_offers", ["availability"])
    op.create_index("ix_marketplace_offers_created_at", "marketplace_offers", ["created_at"])

    op.create_table(
        "scoring_runs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("score_total", sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column("score_trend", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("score_seo", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("score_commercial", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("score_confidence", sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_scoring_runs_product_id", "scoring_runs", ["product_id"])
    op.create_index("ix_scoring_runs_created_at", "scoring_runs", ["created_at"])

    op.create_table(
        "ai_content_drafts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("seo_page_id", sa.Integer(), nullable=True),
        sa.Column("product_id", sa.Integer(), nullable=True),
        sa.Column("draft_type", sa.String(length=80), nullable=False),
        sa.Column("content_json", sa.JSON(), nullable=False),
        sa.Column("confidence_level", sa.String(length=50), nullable=False),
        sa.Column("review_status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["seo_page_id"], ["seo_pages.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_content_drafts_seo_page_id", "ai_content_drafts", ["seo_page_id"])
    op.create_index("ix_ai_content_drafts_product_id", "ai_content_drafts", ["product_id"])
    op.create_index("ix_ai_content_drafts_draft_type", "ai_content_drafts", ["draft_type"])
    op.create_index("ix_ai_content_drafts_review_status", "ai_content_drafts", ["review_status"])
    op.create_index("ix_ai_content_drafts_created_at", "ai_content_drafts", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_ai_content_drafts_created_at", table_name="ai_content_drafts")
    op.drop_index("ix_ai_content_drafts_review_status", table_name="ai_content_drafts")
    op.drop_index("ix_ai_content_drafts_draft_type", table_name="ai_content_drafts")
    op.drop_index("ix_ai_content_drafts_product_id", table_name="ai_content_drafts")
    op.drop_index("ix_ai_content_drafts_seo_page_id", table_name="ai_content_drafts")
    op.drop_table("ai_content_drafts")

    op.drop_index("ix_scoring_runs_created_at", table_name="scoring_runs")
    op.drop_index("ix_scoring_runs_product_id", table_name="scoring_runs")
    op.drop_table("scoring_runs")

    op.drop_index("ix_marketplace_offers_created_at", table_name="marketplace_offers")
    op.drop_index("ix_marketplace_offers_availability", table_name="marketplace_offers")
    op.drop_index("ix_marketplace_offers_marketplace", table_name="marketplace_offers")
    op.drop_index("ix_marketplace_offers_product_id", table_name="marketplace_offers")
    op.drop_table("marketplace_offers")

    op.drop_index("ix_trend_snapshots_created_at", table_name="trend_snapshots")
    op.drop_index("ix_trend_snapshots_source_name", table_name="trend_snapshots")
    op.drop_index("ix_trend_snapshots_keyword_id", table_name="trend_snapshots")
    op.drop_index("ix_trend_snapshots_product_id", table_name="trend_snapshots")
    op.drop_table("trend_snapshots")

    op.drop_index("ix_product_sources_created_at", table_name="product_sources")
    op.drop_index("ix_product_sources_source_name", table_name="product_sources")
    op.drop_index("ix_product_sources_product_id", table_name="product_sources")
    op.drop_table("product_sources")

    op.drop_index("ix_seo_pages_created_at", table_name="seo_pages")
    op.drop_index("ix_seo_pages_status", table_name="seo_pages")
    op.drop_index("ix_seo_pages_slug", table_name="seo_pages")
    op.drop_index("ix_seo_pages_page_type", table_name="seo_pages")
    op.drop_table("seo_pages")

    op.drop_index("ix_keywords_created_at", table_name="keywords")
    op.drop_index("ix_keywords_status", table_name="keywords")
    op.drop_index("ix_keywords_category", table_name="keywords")
    op.drop_index("ix_keywords_keyword", table_name="keywords")
    op.drop_table("keywords")

    op.drop_index("ix_products_created_at", table_name="products")
    op.drop_index("ix_products_status", table_name="products")
    op.drop_index("ix_products_category", table_name="products")
    op.drop_index("ix_products_slug", table_name="products")
    op.drop_table("products")
