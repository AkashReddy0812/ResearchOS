from fastapi import APIRouter, Depends, status

from app.ai.shared.schemas import ResearchResponse
from app.api.v1.auth.dependencies import get_current_user
from app.db.models.user import User
from app.schemas.research import ResearchRequest
from app.services.research_service import ResearchService

router = APIRouter(
    prefix="/research",
    tags=["Research"],
)


@router.post(
    "",
    response_model=ResearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Execute an AI-powered research workflow",
)
async def research(
    request: ResearchRequest,
    current_user: User = Depends(get_current_user),
) -> ResearchResponse:
    """
    Executes the complete ResearchOS workflow.

    Requires JWT authentication.
    """

    service = ResearchService()

    return await service.research(request.query)    