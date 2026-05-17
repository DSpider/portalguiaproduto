from fastapi import APIRouter, Depends

from app.repositories.products import ProductRepository
from app.schemas.product import ProductDetail, ProductSummary
from app.services.products import ProductService

router = APIRouter(prefix="/products", tags=["products"])


def get_product_service() -> ProductService:
    return ProductService(repository=ProductRepository())


@router.get("", response_model=list[ProductSummary])
def list_products(
    service: ProductService = Depends(get_product_service),
) -> list[ProductSummary]:
    return service.list_products()


@router.get("/{slug}", response_model=ProductDetail)
def get_product(
    slug: str,
    service: ProductService = Depends(get_product_service),
) -> ProductDetail:
    return service.get_product_by_slug(slug)
