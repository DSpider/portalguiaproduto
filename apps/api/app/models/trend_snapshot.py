from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import JSON, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.product import utc_now


class TrendSnapshot(Base):
    __tablename__ = "trend_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int | None] = mapped_column(
        ForeignKey("products.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    keyword_id: Mapped[int | None] = mapped_column(
        ForeignKey("keywords.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    source_name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    trend_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    search_interest: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)
    period_start: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    period_end: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    raw_payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        index=True,
    )

    product = relationship("Product", back_populates="trend_snapshots")
    keyword = relationship("Keyword", back_populates="trend_snapshots")
