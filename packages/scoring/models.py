from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


Recommendation = Literal[
    "criar_pagina",
    "atualizar_pagina",
    "monitorar",
    "ignorar_por_enquanto",
]


@dataclass(frozen=True)
class ScoreInput:
    trend_growth_percent: float | None
    estimated_search_volume: int | None
    seo_competition: float | None
    marketplace_availability: float | None
    price_competitiveness: float | None
    average_rating: float | None
    reviews_count: int | None
    commission_rate_percent: float | None
    data_age_days: int | None
    source_confidence: float | None

    def missing_fields(self) -> list[str]:
        return [
            field_name
            for field_name, value in self.__dict__.items()
            if value is None
        ]

    def completeness_score(self) -> float:
        total_fields = len(self.__dict__)
        missing_count = len(self.missing_fields())
        return ((total_fields - missing_count) / total_fields) * 100.0


@dataclass(frozen=True)
class ScoreResult:
    score_total: float
    score_trend: float
    score_seo: float
    score_commercial: float
    score_confidence: float
    recommendation: Recommendation
    human_explanation: str
