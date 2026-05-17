from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ThinContentResult:
    is_thin: bool
    reasons: list[str]


def validate_content_depth(
    *,
    word_count: int,
    unique_products_count: int,
    sources_count: int,
    has_update_date: bool,
    has_original_criteria: bool,
    min_words: int = 450,
) -> ThinContentResult:
    reasons: list[str] = []

    if word_count < min_words:
        reasons.append("conteudo_curto")
    if unique_products_count < 1:
        reasons.append("sem_produtos_validos")
    if sources_count < 1:
        reasons.append("sem_fontes")
    if not has_update_date:
        reasons.append("sem_data_atualizacao")
    if not has_original_criteria:
        reasons.append("sem_criterios_originais")

    return ThinContentResult(is_thin=bool(reasons), reasons=reasons)
