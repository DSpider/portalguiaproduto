from fastapi import APIRouter, Depends

from app.core.security import require_admin_auth
from app.schemas.content import BriefingRequest, BriefingResponse
from app.services.content_briefing import ContentBriefingService

router = APIRouter(prefix="/content", tags=["content"])


def get_content_briefing_service() -> ContentBriefingService:
    return ContentBriefingService()


@router.post("/briefing", response_model=BriefingResponse)
def create_content_briefing(
    payload: BriefingRequest,
    _: None = Depends(require_admin_auth),
    service: ContentBriefingService = Depends(get_content_briefing_service),
) -> BriefingResponse:
    return service.generate(payload)
