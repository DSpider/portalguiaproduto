from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.product import utc_now


class ScoringRun(Base):
    __tablename__ = "scoring_runs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    score_total: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    score_trend: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    score_seo: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    score_commercial: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    score_confidence: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        index=True,
    )

    product = relationship("Product", back_populates="scoring_runs")
