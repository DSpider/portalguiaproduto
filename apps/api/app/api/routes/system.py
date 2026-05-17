from fastapi import APIRouter

from app.core.config import Settings, get_settings
from app.schemas.system import HealthResponse, VersionResponse

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        service=settings.project_slug,
        environment=settings.app_env,
    )


@router.get("/version", response_model=VersionResponse)
def version() -> VersionResponse:
    settings: Settings = get_settings()
    return VersionResponse(
        project=settings.project_name,
        service=settings.project_slug,
        environment=settings.app_env,
        version=settings.app_version,
    )
