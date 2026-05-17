from fastapi import APIRouter

from app.api.v1.endpoints import content, products, radar

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(radar.router)
api_router.include_router(products.router)
api_router.include_router(content.router)
