from app.schemas.product import ProductDetail


class ProductRepository:
    def __init__(self) -> None:
        self._products = [
            ProductDetail(
                slug="notebook-ultrafino-14",
                name="Notebook Ultrafino 14",
                brand="Marca Demo",
                category="notebooks",
                trend_score=87,
                confidence="mock",
                summary="Produto mockado para validar o fluxo inicial da API.",
                data_sources=["mock"],
                last_updated="2026-05-16",
            ),
            ProductDetail(
                slug="fone-bluetooth-custo-beneficio",
                name="Fone Bluetooth Custo-Beneficio",
                brand="Audio Demo",
                category="audio",
                trend_score=81,
                confidence="mock",
                summary="Produto mockado para testes de listagem e detalhe.",
                data_sources=["mock"],
                last_updated="2026-05-16",
            ),
            ProductDetail(
                slug="smartwatch-entrada",
                name="Smartwatch de Entrada",
                brand="Wear Demo",
                category="wearables",
                trend_score=74,
                confidence="mock",
                summary="Produto mockado para representar uma oportunidade inicial.",
                data_sources=["mock"],
                last_updated="2026-05-16",
            ),
        ]

    def list_products(self) -> list[ProductDetail]:
        return self._products

    def get_by_slug(self, slug: str) -> ProductDetail | None:
        return next(
            (product for product in self._products if product.slug == slug),
            None,
        )
