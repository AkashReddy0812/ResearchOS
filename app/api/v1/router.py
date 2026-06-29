from fastapi import APIRouter

from app.api.v1.auth.router import router as auth_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.research import router as research_router

router = APIRouter()

router.include_router(health_router)
router.include_router(auth_router)
router.include_router(research_router)