from __future__ import annotations

from typing import Any

from packages.seo import (
    OfferData,
    ProductSchemaInput,
    ReviewData,
    generate_breadcrumb_schema,
    generate_breadcrumbs,
    generate_canonical_url,
    generate_faq,
    generate_faq_schema,
    generate_heading_structure,
    generate_meta_description,
    generate_product_schema,
    generate_seo_title,
    generate_slug,
)

from app.schemas.content import BriefingOfferInput, BriefingRequest, BriefingResponse


class ContentBriefingService:
    def generate(self, payload: BriefingRequest) -> BriefingResponse:
        slug = generate_slug(payload.palavra_chave_principal)
        canonical_url = str(
            payload.produto.url
            or generate_canonical_url(str(payload.site_base_url), payload.palavra_chave_principal)
        )
        updated_at = payload.produto.updated_at

        title_seo = generate_seo_title(
            payload.palavra_chave_principal,
            "ranking",
        )
        meta_description = generate_meta_description(
            payload.palavra_chave_principal,
            "ranking",
            updated_at=updated_at,
        )
        headings = generate_heading_structure(payload.palavra_chave_principal, "ranking")
        criteria = self._known_criteria(payload)
        faq_items = generate_faq(payload.palavra_chave_principal, "ranking", criteria)
        reliable_offer = self._first_reliable_offer(payload.ofertas_disponiveis)
        rating = payload.dados_de_avaliacao
        review_is_reliable = bool(
            rating
            and rating.source_is_reliable
            and rating.rating_average is not None
            and rating.reviews_count is not None
            and rating.reviews_count > 0
        )

        schema_json_ld = self._build_schema_json_ld(
            payload=payload,
            canonical_url=canonical_url,
            reliable_offer=reliable_offer,
            review=ReviewData(
                rating_value=rating.rating_average if review_is_reliable and rating else None,
                review_count=rating.reviews_count if review_is_reliable and rating else None,
                source_is_reliable=review_is_reliable,
                tested_by_guia_produto=payload.produto.tested_by_guia_produto,
            ),
            faq_items=faq_items,
        )

        alerts = self._build_review_alerts(payload, reliable_offer, review_is_reliable, faq_items)
        confidence_level = self._confidence_level(payload, alerts)

        return BriefingResponse(
            title_seo=title_seo,
            meta_description=meta_description,
            slug=slug,
            h1=headings.h1,
            outline={
                "h2": headings.h2,
                "h3": headings.h3,
            },
            resumo_curto=self._build_short_summary(payload),
            pontos_positivos=self._build_positive_points(payload, reliable_offer, review_is_reliable),
            pontos_negativos=self._build_negative_points(payload, reliable_offer, review_is_reliable),
            para_quem_serve=self._build_fit(payload),
            para_quem_nao_serve=self._build_not_fit(payload),
            ficha_tecnica=payload.produto.ficha_tecnica,
            faq=[
                {
                    "pergunta": item.question,
                    "resposta": item.answer,
                }
                for item in faq_items
            ],
            schema_json_ld=schema_json_ld,
            recomendacao_editorial=self._editorial_recommendation(payload, alerts),
            nivel_de_confianca=confidence_level,
            alertas_de_revisao=alerts,
        )

    def _first_reliable_offer(self, offers: list[BriefingOfferInput]) -> BriefingOfferInput | None:
        for offer in offers:
            if offer.price_is_reliable and offer.price is not None:
                return offer
        return None

    def _known_criteria(self, payload: BriefingRequest) -> list[str]:
        criteria = ["tendencia", "confiabilidade dos dados"]
        if payload.ofertas_disponiveis:
            criteria.append("disponibilidade em marketplace")
        if any(offer.price_is_reliable and offer.price is not None for offer in payload.ofertas_disponiveis):
            criteria.append("preco verificado")
        if payload.dados_de_avaliacao and payload.dados_de_avaliacao.source_is_reliable:
            criteria.append("avaliacao com fonte confiavel")
        if payload.score_calculado and payload.score_calculado.score_total is not None:
            criteria.append("score calculado")
        return criteria

    def _build_schema_json_ld(
        self,
        *,
        payload: BriefingRequest,
        canonical_url: str,
        reliable_offer: BriefingOfferInput | None,
        review: ReviewData,
        faq_items: list[Any],
    ) -> list[dict[str, Any]]:
        product_schema = generate_product_schema(
            ProductSchemaInput(
                name=payload.produto.name,
                brand=payload.produto.brand,
                description=payload.produto.description,
                image_url=str(payload.produto.image_url) if payload.produto.image_url else None,
                url=canonical_url,
                updated_at=payload.produto.updated_at,
                offer=OfferData(
                    price=reliable_offer.price if reliable_offer else None,
                    currency=reliable_offer.currency if reliable_offer else "BRL",
                    availability=reliable_offer.availability if reliable_offer else None,
                    url=str(reliable_offer.affiliate_url) if reliable_offer and reliable_offer.affiliate_url else None,
                    price_is_reliable=bool(reliable_offer),
                    last_checked_at=reliable_offer.last_checked_at if reliable_offer else None,
                ),
                review=review,
            )
        )

        breadcrumbs = generate_breadcrumbs(
            str(payload.site_base_url),
            [
                ("Tecnologia", "tecnologia"),
                (payload.categoria, payload.categoria),
                (payload.palavra_chave_principal, payload.palavra_chave_principal),
            ],
        )
        schema_json_ld = [
            product_schema,
            generate_breadcrumb_schema(breadcrumbs),
        ]
        faq_schema = generate_faq_schema(faq_items)
        if faq_schema:
            schema_json_ld.append(faq_schema)
        return schema_json_ld

    def _build_short_summary(self, payload: BriefingRequest) -> str:
        trend_text = ""
        if payload.tendencia and payload.tendencia.trend_growth_percent is not None:
            trend_text = f" O sinal de tendencia informado e de {payload.tendencia.trend_growth_percent:.1f}%."

        return (
            f"Rascunho editorial para revisar uma pagina sobre {payload.palavra_chave_principal}, "
            f"na categoria {payload.categoria}, com foco no produto {payload.produto.name}."
            f"{trend_text} Este texto nao deve ser publicado sem revisao humana."
        )

    def _build_positive_points(
        self,
        payload: BriefingRequest,
        reliable_offer: BriefingOfferInput | None,
        review_is_reliable: bool,
    ) -> list[str]:
        points: list[str] = []
        if payload.tendencia and payload.tendencia.trend_growth_percent and payload.tendencia.trend_growth_percent > 20:
            points.append("Tendencia positiva informada nos dados de entrada.")
        if reliable_offer:
            points.append("Ha oferta com preco marcado como confiavel.")
        if review_is_reliable:
            points.append("Ha dados de avaliacao com fonte marcada como confiavel.")
        if payload.score_calculado and payload.score_calculado.score_total and payload.score_calculado.score_total >= 60:
            points.append("Score calculado indica oportunidade editorial.")
        if not points:
            points.append("Ha dados suficientes para iniciar um rascunho, mas os pontos fortes precisam de revisao.")
        return points

    def _build_negative_points(
        self,
        payload: BriefingRequest,
        reliable_offer: BriefingOfferInput | None,
        review_is_reliable: bool,
    ) -> list[str]:
        points: list[str] = []
        if not reliable_offer:
            points.append("Nao ha preco confiavel para usar no texto ou no schema.")
        if not review_is_reliable:
            points.append("Nao ha avaliacao confiavel para usar como nota ou aggregateRating.")
        if not payload.concorrentes:
            points.append("Concorrentes nao foram informados.")
        if not payload.produto.ficha_tecnica:
            points.append("Ficha tecnica nao foi informada.")
        return points

    def _build_fit(self, payload: BriefingRequest) -> list[str]:
        return [
            f"Leitores pesquisando {payload.palavra_chave_principal}.",
            f"Usuarios comparando produtos da categoria {payload.categoria}.",
            "Equipe editorial que precisa priorizar atualizacoes com base em sinais estruturados.",
        ]

    def _build_not_fit(self, payload: BriefingRequest) -> list[str]:
        return [
            "Quem precisa de um review pratico ja testado pela equipe.",
            "Quem precisa de preco final se nao houver oferta confiavel informada.",
            f"Quem busca recomendacao definitiva sem revisar os dados de {payload.produto.name}.",
        ]

    def _build_review_alerts(
        self,
        payload: BriefingRequest,
        reliable_offer: BriefingOfferInput | None,
        review_is_reliable: bool,
        faq_items: list[Any],
    ) -> list[str]:
        alerts = [
            "rascunho_requer_revisao_humana",
            "nao_publicar_automaticamente",
        ]

        if not reliable_offer:
            alerts.append("preco_pendente_ou_nao_confiavel")
        if not review_is_reliable:
            alerts.append("avaliacao_pendente_ou_nao_confiavel")
        if not payload.produto.tested_by_guia_produto:
            alerts.append("nao_afirmar_teste_pratico")
        if not payload.produto.ficha_tecnica:
            alerts.append("ficha_tecnica_pendente")
        if not payload.concorrentes:
            alerts.append("concorrentes_pendentes")
        if not faq_items:
            alerts.append("faq_pendente_por_falta_de_criterios")
        if payload.score_calculado is None:
            alerts.append("score_calculado_pendente")

        return alerts

    def _confidence_level(self, payload: BriefingRequest, alerts: list[str]) -> str:
        if payload.score_calculado and payload.score_calculado.score_confidence is not None:
            confidence = payload.score_calculado.score_confidence
        else:
            confidence = max(0.0, 100.0 - (len(alerts) * 10.0))

        if confidence >= 75 and len(alerts) <= 3:
            return "alto"
        if confidence >= 50:
            return "medio"
        return "baixo"

    def _editorial_recommendation(self, payload: BriefingRequest, alerts: list[str]) -> str:
        if payload.score_calculado and payload.score_calculado.recommendation:
            base = payload.score_calculado.recommendation
        elif payload.score_calculado and payload.score_calculado.score_total and payload.score_calculado.score_total >= 60:
            base = "avaliar_atualizacao"
        else:
            base = "monitorar"

        return (
            f"{base}: manter como rascunho editorial ate revisar os alertas "
            f"({', '.join(alerts)})."
        )
