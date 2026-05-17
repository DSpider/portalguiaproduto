from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class BriefingProductInput(BaseModel):
    name: str = Field(min_length=2)
    brand: str | None = None
    description: str | None = None
    image_url: HttpUrl | None = None
    url: HttpUrl | None = None
    updated_at: str | None = None
    ficha_tecnica: dict[str, str] = Field(default_factory=dict)
    tested_by_guia_produto: bool = False


class BriefingTrendInput(BaseModel):
    trend_growth_percent: float | None = None
    search_interest: float | None = None
    source_name: str | None = None
    period: str | None = None


class BriefingOfferInput(BaseModel):
    marketplace: str
    title: str
    price: float | None = None
    currency: str = "BRL"
    affiliate_url: HttpUrl | None = None
    availability: str | None = None
    price_is_reliable: bool = False
    last_checked_at: str | None = None


class BriefingRatingInput(BaseModel):
    rating_average: float | None = Field(default=None, ge=0, le=5)
    reviews_count: int | None = Field(default=None, ge=0)
    source_name: str | None = None
    source_is_reliable: bool = False


class BriefingCompetitorInput(BaseModel):
    name: str
    url: HttpUrl | None = None
    note: str | None = None


class BriefingScoreInput(BaseModel):
    score_total: float | None = Field(default=None, ge=0, le=100)
    score_trend: float | None = Field(default=None, ge=0, le=100)
    score_seo: float | None = Field(default=None, ge=0, le=100)
    score_commercial: float | None = Field(default=None, ge=0, le=100)
    score_confidence: float | None = Field(default=None, ge=0, le=100)
    recommendation: str | None = None
    human_explanation: str | None = None


class BriefingRequest(BaseModel):
    produto: BriefingProductInput
    categoria: str = Field(min_length=2)
    palavra_chave_principal: str = Field(min_length=2)
    palavras_chave_secundarias: list[str] = Field(default_factory=list)
    tendencia: BriefingTrendInput | None = None
    ofertas_disponiveis: list[BriefingOfferInput] = Field(default_factory=list)
    dados_de_avaliacao: BriefingRatingInput | None = None
    concorrentes: list[BriefingCompetitorInput] = Field(default_factory=list)
    score_calculado: BriefingScoreInput | None = None
    site_base_url: HttpUrl = "https://www.guiaproduto.com.br"


class BriefingResponse(BaseModel):
    title_seo: str
    meta_description: str
    slug: str
    h1: str
    outline: dict[str, Any]
    resumo_curto: str
    pontos_positivos: list[str]
    pontos_negativos: list[str]
    para_quem_serve: list[str]
    para_quem_nao_serve: list[str]
    ficha_tecnica: dict[str, str]
    faq: list[dict[str, str]]
    schema_json_ld: list[dict[str, Any]]
    recomendacao_editorial: str
    nivel_de_confianca: str
    alertas_de_revisao: list[str]
