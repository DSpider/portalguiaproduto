from app.repositories.products import ProductRepository
from app.schemas.product import ProductSummary
from app.schemas.radar import RadarSummary


class RadarService:
    def __init__(self, product_repository: ProductRepository) -> None:
        self.product_repository = product_repository

    def get_summary(self) -> RadarSummary:
        products = self.product_repository.list_products()
        highlighted = sorted(
            products,
            key=lambda product: product.trend_score,
            reverse=True,
        )[:3]
        categories = sorted({product.category for product in products})

        return RadarSummary(
            status="ok",
            mode="mock",
            generated_at="2026-05-16T00:00:00-03:00",
            total_products=len(products),
            top_categories=categories,
            highlighted_products=[
                ProductSummary(
                    slug=product.slug,
                    name=product.name,
                    brand=product.brand,
                    category=product.category,
                    trend_score=product.trend_score,
                    confidence=product.confidence,
                )
                for product in highlighted
            ],
        )
