from app.core.errors import NotFoundError
from app.repositories.products import ProductRepository
from app.schemas.product import ProductDetail, ProductSummary


class ProductService:
    def __init__(self, repository: ProductRepository) -> None:
        self.repository = repository

    def list_products(self) -> list[ProductSummary]:
        return [
            ProductSummary(
                slug=product.slug,
                name=product.name,
                brand=product.brand,
                category=product.category,
                trend_score=product.trend_score,
                confidence=product.confidence,
            )
            for product in self.repository.list_products()
        ]

    def get_product_by_slug(self, slug: str) -> ProductDetail:
        product = self.repository.get_by_slug(slug)
        if product is None:
            raise NotFoundError(f"Produto com slug '{slug}' nao encontrado.")
        return product
