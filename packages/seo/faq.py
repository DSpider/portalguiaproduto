from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FAQItem:
    question: str
    answer: str


def generate_faq(
    keyword: str,
    page_type: str,
    known_criteria: list[str],
    max_items: int = 4,
) -> list[FAQItem]:
    keyword = keyword.strip()
    criteria = [item.strip() for item in known_criteria if item.strip()]

    if len(criteria) < 2:
        return []

    faq = [
        FAQItem(
            question=f"Como comparar {keyword}?",
            answer=f"Compare {keyword} usando criterios como {', '.join(criteria[:3])}. Evite decidir apenas por preco quando os dados forem incompletos.",
        ),
        FAQItem(
            question=f"Quando vale atualizar uma pagina sobre {keyword}?",
            answer="Vale atualizar quando houver mudanca relevante em tendencia, disponibilidade, preco confiavel ou novas informacoes verificadas.",
        ),
    ]

    if page_type == "ranking":
        faq.append(
            FAQItem(
                question=f"O ranking de {keyword} usa preco como criterio?",
                answer="Preco pode ser considerado somente quando houver fonte confiavel e data de verificacao. Sem esse dado, o preco nao deve aparecer como criterio decisivo.",
            )
        )

    return faq[:max_items]
