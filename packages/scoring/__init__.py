"""Motor de Trend Score do Guia Produto Radar."""

from packages.scoring.calculator import calculate_trend_score
from packages.scoring.models import Recommendation, ScoreInput, ScoreResult

__all__ = [
    "Recommendation",
    "ScoreInput",
    "ScoreResult",
    "calculate_trend_score",
]
