from fastapi import APIRouter

from app.schemas.base import SuccessResponse
from app.schemas.health import HealthData

router = APIRouter()


@router.get("/health", response_model=SuccessResponse[HealthData])
async def health_check() -> SuccessResponse[HealthData]:
    return SuccessResponse(
        message="Service is healthy",
        data=HealthData(
            status="healthy",
            service="ResearchOS",
        ),
    )