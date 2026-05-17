from fastapi import APIRouter, Depends

from app.repositories.products import ProductRepository
from app.schemas.radar import RadarSummary
from app.services.radar import RadarService

router = APIRouter(prefix="/radar", tags=["radar"])


def get_radar_service() -> RadarService:
    return RadarService(product_repository=ProductRepository())


@router.get("/summary", response_model=RadarSummary)
def radar_summary(
    service: RadarService = Depends(get_radar_service),
) -> RadarSummary:
    return service.get_summary()
