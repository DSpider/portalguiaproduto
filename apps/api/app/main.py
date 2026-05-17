from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.system import router as system_router
from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.errors import register_error_handlers


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title=settings.project_name,
        version=settings.app_version,
        description="API base do Guia Produto Radar.",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.admin_cors_origin_list,
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type"],
    )

    register_error_handlers(application)
    application.include_router(system_router)
    application.include_router(api_router)

    @application.get("/", tags=["system"])
    def root() -> dict[str, str]:
        return {
            "service": settings.project_slug,
            "status": "running",
        }

    return application


app = create_app()
