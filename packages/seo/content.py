from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HeadingStructure:
    h1: str
    h2: list[str]
    h3: dict[str, list[str]]


def generate_heading_structure(
    keyword: str,
    page_type: str,
    include_faq: bool = True,
) -> HeadingStructure:
    keyword = keyword.strip()
    if page_type == "ranking":
        h1 = f"Melhores {keyword}"
        h2 = [
            "Como avaliamos as opcoes",
            "Ranking de produtos",
            "Como escolher",
        ]
        h3 = {
            "Como avaliamos as opcoes": ["Tendencia", "Oferta e disponibilidade", "Confiabilidade dos dados"],
            "Ranking de produtos": ["Destaques", "Pontos de atencao"],
            "Como escolher": ["Perfil de uso", "Criterios antes da compra"],
        }
    elif page_type == "comparativo":
        h1 = f"Comparativo: {keyword}"
        h2 = ["Resumo das diferencas", "Tabela comparativa", "Qual escolher"]
        h3 = {
            "Resumo das diferencas": ["Pontos fortes", "Limites"],
            "Tabela comparativa": ["Especificacoes", "Preco e disponibilidade"],
            "Qual escolher": ["Melhor para cada perfil"],
        }
    else:
        h1 = keyword
        h2 = ["Visao geral", "Criterios de analise", "Pontos de atencao"]
        h3 = {
            "Visao geral": ["Contexto"],
            "Criterios de analise": ["Dados usados", "Limites dos dados"],
            "Pontos de atencao": ["Antes de comprar"],
        }

    if include_faq:
        h2.append("Perguntas frequentes")
        h3["Perguntas frequentes"] = ["Duvidas comuns"]

    return HeadingStructure(h1=h1, h2=h2, h3=h3)
