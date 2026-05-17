from __future__ import annotations

import math

from packages.scoring.config import ScoringConfig, load_default_config
from packages.scoring.models import Recommendation, ScoreInput, ScoreResult


def calculate_trend_score(
    score_input: ScoreInput,
    config: ScoringConfig | None = None,
) -> ScoreResult:
    scoring_config = config or load_default_config()

    normalized = _normalize_input(score_input, scoring_config)

    score_trend = _weighted_average(
        {
            "trend_growth": normalized["trend_growth"],
        },
        scoring_config.component_weights["trend"],
    )
    score_seo = _weighted_average(
        {
            "search_volume": normalized["search_volume"],
            "seo_opportunity": normalized["seo_opportunity"],
        },
        scoring_config.component_weights["seo"],
    )
    score_commercial = _weighted_average(
        {
            "marketplace_availability": normalized["marketplace_availability"],
            "price_competitiveness": normalized["price_competitiveness"],
            "average_rating": normalized["average_rating"],
            "reviews_count": normalized["reviews_count"],
            "commission_potential": normalized["commission_potential"],
        },
        scoring_config.component_weights["commercial"],
    )
    score_confidence = _weighted_average(
        {
            "data_recency": normalized["data_recency"],
            "source_confidence": normalized["source_confidence"],
            "data_completeness": normalized["data_completeness"],
        },
        scoring_config.component_weights["confidence"],
    )

    score_total = _weighted_average(
        {
            "trend": score_trend,
            "seo": score_seo,
            "commercial": score_commercial,
            "confidence": score_confidence,
        },
        scoring_config.total_weights,
    )

    recommendation = _recommend(score_total, score_confidence, scoring_config)
    human_explanation = _build_explanation(
        score_total=score_total,
        score_trend=score_trend,
        score_seo=score_seo,
        score_commercial=score_commercial,
        score_confidence=score_confidence,
        recommendation=recommendation,
        missing_fields=score_input.missing_fields(),
    )

    return ScoreResult(
        score_total=round(score_total, 2),
        score_trend=round(score_trend, 2),
        score_seo=round(score_seo, 2),
        score_commercial=round(score_commercial, 2),
        score_confidence=round(score_confidence, 2),
        recommendation=recommendation,
        human_explanation=human_explanation,
    )


def _normalize_input(score_input: ScoreInput, config: ScoringConfig) -> dict[str, float]:
    return {
        "trend_growth": _normalize_linear(
            score_input.trend_growth_percent,
            config.normalization["trend_growth_min_percent"],
            config.normalization["trend_growth_max_percent"],
        ),
        "search_volume": _normalize_log(
            score_input.estimated_search_volume,
            config.normalization["search_volume_cap"],
        ),
        "seo_opportunity": 100.0 - _clamp(score_input.seo_competition or 0.0),
        "marketplace_availability": _clamp((score_input.marketplace_availability or 0.0) * 100.0),
        "price_competitiveness": _clamp(score_input.price_competitiveness or 0.0),
        "average_rating": _clamp(((score_input.average_rating or 0.0) / 5.0) * 100.0),
        "reviews_count": _normalize_log(
            score_input.reviews_count,
            config.normalization["reviews_count_cap"],
        ),
        "commission_potential": _normalize_linear(
            score_input.commission_rate_percent,
            0.0,
            config.normalization["commission_rate_cap_percent"],
        ),
        "data_recency": _normalize_recency(
            score_input.data_age_days,
            config.normalization["fresh_until_days"],
            config.normalization["stale_after_days"],
        ),
        "source_confidence": _clamp((score_input.source_confidence or 0.0) * 100.0),
        "data_completeness": score_input.completeness_score(),
    }


def _recommend(
    score_total: float,
    score_confidence: float,
    config: ScoringConfig,
) -> Recommendation:
    thresholds = config.recommendation_thresholds

    if score_total >= thresholds["create_page"] and score_confidence >= thresholds["minimum_confidence_for_action"]:
        return "criar_pagina"
    if score_total >= thresholds["update_page"] and score_confidence >= thresholds["minimum_confidence_for_action"]:
        return "atualizar_pagina"
    if score_total >= thresholds["monitor"]:
        return "monitorar"
    return "ignorar_por_enquanto"


def _build_explanation(
    *,
    score_total: float,
    score_trend: float,
    score_seo: float,
    score_commercial: float,
    score_confidence: float,
    recommendation: Recommendation,
    missing_fields: list[str],
) -> str:
    parts = [
        f"Score total {score_total:.1f}/100.",
        f"Tendencia {score_trend:.1f}, SEO {score_seo:.1f}, comercial {score_commercial:.1f} e confianca {score_confidence:.1f}.",
    ]

    if recommendation == "criar_pagina":
        parts.append("Recomendacao: criar pagina porque os sinais combinados estao fortes e confiaveis.")
    elif recommendation == "atualizar_pagina":
        parts.append("Recomendacao: atualizar pagina porque ha oportunidade razoavel com confianca suficiente.")
    elif recommendation == "monitorar":
        parts.append("Recomendacao: monitorar porque os sinais ainda nao justificam uma acao editorial forte.")
    else:
        parts.append("Recomendacao: ignorar por enquanto porque os sinais sao fracos ou pouco confiaveis.")

    if missing_fields:
        parts.append("Campos ausentes reduzem a confianca: " + ", ".join(missing_fields) + ".")

    return " ".join(parts)


def _weighted_average(scores: dict[str, float], weights: dict[str, float]) -> float:
    total_weight = sum(weights.values())
    if total_weight <= 0:
        return 0.0

    weighted_sum = sum(scores[key] * weights[key] for key in weights)
    return _clamp(weighted_sum / total_weight)


def _normalize_linear(value: float | int | None, min_value: float, max_value: float) -> float:
    if value is None or max_value <= min_value:
        return 0.0
    normalized = ((float(value) - min_value) / (max_value - min_value)) * 100.0
    return _clamp(normalized)


def _normalize_log(value: float | int | None, cap: float) -> float:
    if value is None or value <= 0 or cap <= 0:
        return 0.0
    normalized = (math.log10(float(value) + 1.0) / math.log10(cap + 1.0)) * 100.0
    return _clamp(normalized)


def _normalize_recency(value: float | int | None, fresh_until_days: float, stale_after_days: float) -> float:
    if value is None:
        return 0.0
    age = float(value)
    if age <= fresh_until_days:
        return 100.0
    if age >= stale_after_days:
        return 0.0
    return _clamp(100.0 * (1.0 - ((age - fresh_until_days) / (stale_after_days - fresh_until_days))))


def _clamp(value: float) -> float:
    return max(0.0, min(100.0, float(value)))
