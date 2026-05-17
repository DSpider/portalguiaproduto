from packages.scoring import ScoreInput, calculate_trend_score


def test_strong_opportunity_recommends_create_page() -> None:
    result = calculate_trend_score(
        ScoreInput(
            trend_growth_percent=82.0,
            estimated_search_volume=42000,
            seo_competition=22.0,
            marketplace_availability=1.0,
            price_competitiveness=92.0,
            average_rating=4.8,
            reviews_count=920,
            commission_rate_percent=11.0,
            data_age_days=1,
            source_confidence=0.94,
        )
    )

    assert result.score_total >= 75
    assert result.score_confidence >= 55
    assert result.recommendation == "criar_pagina"
    assert "Score total" in result.human_explanation


def test_medium_opportunity_recommends_update_or_monitor() -> None:
    result = calculate_trend_score(
        ScoreInput(
            trend_growth_percent=38.0,
            estimated_search_volume=6500,
            seo_competition=58.0,
            marketplace_availability=0.65,
            price_competitiveness=63.0,
            average_rating=4.1,
            reviews_count=140,
            commission_rate_percent=4.5,
            data_age_days=10,
            source_confidence=0.72,
        )
    )

    assert 40 <= result.score_total < 75
    assert result.recommendation in {"atualizar_pagina", "monitorar"}
    assert result.score_seo > 0
    assert result.score_commercial > 0


def test_weak_opportunity_recommends_ignore() -> None:
    result = calculate_trend_score(
        ScoreInput(
            trend_growth_percent=-15.0,
            estimated_search_volume=80,
            seo_competition=92.0,
            marketplace_availability=0.0,
            price_competitiveness=18.0,
            average_rating=3.0,
            reviews_count=2,
            commission_rate_percent=0.5,
            data_age_days=80,
            source_confidence=0.20,
        )
    )

    assert result.score_total < 40
    assert result.recommendation == "ignorar_por_enquanto"
    assert "sinais sao fracos" in result.human_explanation


def test_missing_data_reduces_confidence_and_is_explained() -> None:
    complete_result = calculate_trend_score(
        ScoreInput(
            trend_growth_percent=70.0,
            estimated_search_volume=30000,
            seo_competition=30.0,
            marketplace_availability=0.9,
            price_competitiveness=80.0,
            average_rating=4.6,
            reviews_count=500,
            commission_rate_percent=8.0,
            data_age_days=2,
            source_confidence=0.85,
        )
    )
    result = calculate_trend_score(
        ScoreInput(
            trend_growth_percent=70.0,
            estimated_search_volume=30000,
            seo_competition=30.0,
            marketplace_availability=None,
            price_competitiveness=None,
            average_rating=None,
            reviews_count=None,
            commission_rate_percent=None,
            data_age_days=2,
            source_confidence=0.85,
        )
    )

    assert result.score_confidence < complete_result.score_confidence
    assert result.recommendation in {"monitorar", "atualizar_pagina"}
    assert "Campos ausentes reduzem a confianca" in result.human_explanation
