from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings


def create_application() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )

    app.include_router(
        api_router,
        prefix="/api",
    )

    return app