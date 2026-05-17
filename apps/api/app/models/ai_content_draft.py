from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.product import utc_now


class AIContentDraft(Base):
    __tablename__ = "ai_content_drafts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    seo_page_id: Mapped[int | None] = mapped_column(
        ForeignKey("seo_pages.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    product_id: Mapped[int | None] = mapped_column(
        ForeignKey("products.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    draft_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    content_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    confidence_level: Mapped[str] = mapped_column(String(50), nullable=False)
    review_status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    seo_page = relationship("SeoPage", back_populates="content_drafts")
    product = relationship("Product", back_populates="content_drafts")
