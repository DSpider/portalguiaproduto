from decimal import Decimal

from packages.seo import (
    BreadcrumbItem,
    OfferData,
    ProductSchemaInput,
    ReviewData,
    generate_breadcrumb_schema,
    generate_breadcrumbs,
    generate_canonical_url,
    generate_meta_description,
    generate_product_schema,
    generate_seo_title,
    generate_slug,
    validate_content_depth,
    validate_json_ld_schema,
)


def test_generate_slug_removes_accents_and_stop_words() -> None:
    assert generate_slug("Melhores Notebooks para Estudar em 2026!") == "melhores-notebooks-estudar-em-2026"


def test_generate_seo_title_is_specific_and_limited() -> None:
    title = generate_seo_title("notebooks leves para estudar", "ranking", year=2026)

    assert title == "Melhores notebooks leves para estudar 2026"
    assert len(title) <= 60


def test_generate_meta_description_includes_update_date() -> None:
    description = generate_meta_description(
        "notebooks leves",
        "ranking",
        updated_at="2026-05-16",
    )

    assert "notebooks leves" in description
    assert "Atualizado em 2026-05-16" in description
    assert len(description) <= 155


def test_generate_product_schema_with_reliable_offer_and_rating() -> None:
    schema = generate_product_schema(
        ProductSchemaInput(
            name="Notebook Demo",
            brand="Marca Demo",
            description="Produto ficticio para validar schema.",
            image_url="https://example.test/notebook.webp",
            url="https://example.test/notebook-demo/",
            updated_at="2026-05-16",
            offer=OfferData(
                price=Decimal("3999.90"),
                currency="BRL",
                availability="InStock",
                url="https://example.test/oferta",
                price_is_reliable=True,
            ),
            review=ReviewData(
                rating_value=4.6,
                review_count=120,
                source_is_reliable=True,
            ),
        )
    )

    assert schema["@type"] == "Product"
    assert schema["offers"]["price"] == "3999.90"
    assert schema["aggregateRating"]["ratingValue"] == 4.6
    assert schema["dateModified"] == "2026-05-16"
    assert "review" not in schema
    assert validate_json_ld_schema(schema) == []


def test_product_schema_does_not_include_unreliable_price() -> None:
    schema = generate_product_schema(
        ProductSchemaInput(
            name="Produto sem preco confiavel",
            url="https://example.test/produto/",
            offer=OfferData(
                price=Decimal("299.90"),
                currency="BRL",
                availability="InStock",
                url="https://example.test/oferta",
                price_is_reliable=False,
            ),
        )
    )

    assert "offers" not in schema


def test_product_schema_does_not_include_unreliable_rating() -> None:
    schema = generate_product_schema(
        ProductSchemaInput(
            name="Produto sem avaliacao confiavel",
            url="https://example.test/produto/",
            review=ReviewData(
                rating_value=4.8,
                review_count=200,
                source_is_reliable=False,
            ),
        )
    )

    assert "aggregateRating" not in schema
    assert "review" not in schema


def test_generate_breadcrumbs_and_schema() -> None:
    breadcrumbs = generate_breadcrumbs(
        "https://www.guiaproduto.com.br",
        [
            ("Tecnologia", "tecnologia"),
            ("Notebooks", "notebooks"),
        ],
    )
    schema = generate_breadcrumb_schema(breadcrumbs)

    assert breadcrumbs[0] == BreadcrumbItem("Inicio", "https://www.guiaproduto.com.br/")
    assert breadcrumbs[-1].url == "https://www.guiaproduto.com.br/notebooks/"
    assert schema["@type"] == "BreadcrumbList"
    assert schema["itemListElement"][2]["position"] == 3
    assert validate_json_ld_schema(schema) == []


def test_generate_canonical_url() -> None:
    assert (
        generate_canonical_url("https://www.guiaproduto.com.br", "Melhores Notebooks")
        == "https://www.guiaproduto.com.br/melhores-notebooks/"
    )


def test_blocks_thin_content() -> None:
    result = validate_content_depth(
        word_count=180,
        unique_products_count=0,
        sources_count=0,
        has_update_date=False,
        has_original_criteria=False,
    )

    assert result.is_thin is True
    assert "conteudo_curto" in result.reasons
    assert "sem_data_atualizacao" in result.reasons
