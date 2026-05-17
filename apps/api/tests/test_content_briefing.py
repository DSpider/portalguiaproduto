from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_content_briefing_with_reliable_data() -> None:
    payload = {
        "produto": {
            "name": "Notebook Demo 14",
            "brand": "Marca Demo",
            "description": "Produto ficticio para validar briefing.",
            "image_url": "https://example.test/notebook.webp",
            "updated_at": "2026-05-16",
            "ficha_tecnica": {
                "Tela": "14 polegadas",
                "Memoria": "16 GB",
            },
        },
        "categoria": "notebooks",
        "palavra_chave_principal": "notebook leve para estudar",
        "palavras_chave_secundarias": ["notebook custo beneficio", "notebook para faculdade"],
        "tendencia": {
            "trend_growth_percent": 42.5,
            "search_interest": 70,
            "source_name": "mock",
            "period": "ultimos 30 dias",
        },
        "ofertas_disponiveis": [
            {
                "marketplace": "mock_marketplace",
                "title": "Oferta mockada",
                "price": 3999.9,
                "currency": "BRL",
                "affiliate_url": "https://example.test/oferta",
                "availability": "InStock",
                "price_is_reliable": True,
                "last_checked_at": "2026-05-16",
            }
        ],
        "dados_de_avaliacao": {
            "rating_average": 4.6,
            "reviews_count": 120,
            "source_name": "mock",
            "source_is_reliable": True,
        },
        "concorrentes": [
            {"name": "Concorrente Demo", "url": "https://example.test/concorrente"}
        ],
        "score_calculado": {
            "score_total": 78,
            "score_trend": 80,
            "score_seo": 74,
            "score_commercial": 76,
            "score_confidence": 82,
            "recommendation": "criar_pagina",
            "human_explanation": "Score mockado.",
        },
    }

    response = client.post("/api/v1/content/briefing", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == "notebook-leve-estudar"
    assert data["h1"] == "Melhores notebook leve para estudar"
    assert data["nivel_de_confianca"] == "alto"
    assert data["recomendacao_editorial"].startswith("criar_pagina")
    assert "rascunho_requer_revisao_humana" in data["alertas_de_revisao"]
    assert "nao_publicar_automaticamente" in data["alertas_de_revisao"]

    product_schema = data["schema_json_ld"][0]
    assert product_schema["@type"] == "Product"
    assert product_schema["offers"]["price"] == "3999.9"
    assert product_schema["aggregateRating"]["ratingValue"] == 4.6
    assert "review" not in product_schema


def test_content_briefing_does_not_invent_price_or_rating() -> None:
    payload = {
        "produto": {
            "name": "Fone Demo",
            "brand": "Audio Demo",
            "description": "Produto ficticio sem preco ou avaliacao confiavel.",
        },
        "categoria": "audio",
        "palavra_chave_principal": "fone bluetooth barato",
        "palavras_chave_secundarias": [],
        "tendencia": {
            "trend_growth_percent": 12,
            "source_name": "mock",
        },
        "ofertas_disponiveis": [
            {
                "marketplace": "mock_marketplace",
                "title": "Oferta sem preco confiavel",
                "price": 199.9,
                "currency": "BRL",
                "price_is_reliable": False,
            }
        ],
        "dados_de_avaliacao": {
            "rating_average": 4.9,
            "reviews_count": 500,
            "source_name": "mock",
            "source_is_reliable": False,
        },
        "concorrentes": [],
        "score_calculado": {
            "score_total": 45,
            "score_confidence": 40,
            "recommendation": "monitorar",
        },
    }

    response = client.post("/api/v1/content/briefing", json=payload)

    assert response.status_code == 200
    data = response.json()
    product_schema = data["schema_json_ld"][0]
    assert "offers" not in product_schema
    assert "aggregateRating" not in product_schema
    assert "review" not in product_schema
    assert data["nivel_de_confianca"] == "baixo"
    assert "preco_pendente_ou_nao_confiavel" in data["alertas_de_revisao"]
    assert "avaliacao_pendente_ou_nao_confiavel" in data["alertas_de_revisao"]
    assert "nao_afirmar_teste_pratico" in data["alertas_de_revisao"]
    assert "ficha_tecnica_pendente" in data["alertas_de_revisao"]


def test_content_briefing_rejects_invalid_payload() -> None:
    response = client.post(
        "/api/v1/content/briefing",
        json={
            "produto": {"name": "A"},
            "categoria": "",
            "palavra_chave_principal": "",
        },
    )

    assert response.status_code == 422
