from __future__ import annotations

from urllib.parse import urljoin

from packages.seo.slug import generate_slug


def generate_seo_title(
    keyword: str,
    page_type: str,
    qualifier: str | None = None,
    year: int | None = None,
    max_length: int = 60,
) -> str:
    label_by_type = {
        "ranking": "Melhores",
        "comparativo": "Comparativo",
        "guia": "Guia",
        "tendencia": "Tendencias",
        "produto": "Analise",
    }
    prefix = label_by_type.get(page_type, "Guia")
    parts = [prefix, keyword.strip()]

    if qualifier:
        parts.append(qualifier.strip())
    if year:
        parts.append(str(year))

    title = " ".join(part for part in parts if part)
    if len(title) <= max_length:
        return title

    return title[:max_length].rsplit(" ", 1)[0].rstrip(" :-")


def generate_meta_description(
    keyword: str,
    page_type: str,
    updated_at: str | None = None,
    max_length: int = 155,
) -> str:
    templates = {
        "ranking": "Compare opcoes de {keyword}, veja criterios de escolha e acompanhe sinais atualizados antes de comprar.",
        "comparativo": "Veja diferencas importantes em {keyword}, com criterios objetivos para apoiar uma decisao de compra.",
        "guia": "Entenda como escolher {keyword}, quais pontos observar e quando vale comparar alternativas.",
        "tendencia": "Acompanhe sinais de tendencia para {keyword}, com dados organizados para priorizar oportunidades.",
        "produto": "Veja informacoes organizadas sobre {keyword}, incluindo criterios de avaliacao e dados disponiveis.",
    }
    description = templates.get(page_type, templates["guia"]).format(keyword=keyword.strip())

    if updated_at:
        description = f"{description} Atualizado em {updated_at}."

    if len(description) <= max_length:
        return description

    return description[:max_length].rsplit(" ", 1)[0].rstrip(" .,") + "."


def generate_canonical_url(base_url: str, path_or_title: str) -> str:
    base = base_url.rstrip("/") + "/"
    slug = generate_slug(path_or_title.strip("/"))
    return urljoin(base, slug + "/")
