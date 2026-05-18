from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.core.security import require_admin_auth
from app.schemas.admin import AdminStatusResponse

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_admin_auth)],
)


@router.get("/status", response_model=AdminStatusResponse)
def admin_status() -> AdminStatusResponse:
    settings: Settings = get_settings()
    return AdminStatusResponse(
        project=settings.project_name,
        service=settings.project_slug,
        environment=settings.app_env,
        version=settings.app_version,
        auth_enabled=settings.admin_auth_enabled,
        auth_mode="admin_token",
    )
