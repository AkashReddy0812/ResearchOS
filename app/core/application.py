from fastapi import FastAPI

from app.core.logging import logger
from app.api.router import api_router
from app.core.config import get_settings
from app.core.lifespan import lifespan
from app.exceptions.handlers import register_exception_handlers
from app.middleware.request_id import RequestIDMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

def create_application() -> FastAPI:
    
    settings = get_settings()

    
    app = FastAPI(
        title=settings.app.name,
        version=settings.app.version,
        lifespan=lifespan,
    )
    register_exception_handlers(app)
    app.add_middleware(RequestIDMiddleware)

    app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,
    )
        
    app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "localhost",
        "127.0.0.1",
    ],
)

    app.include_router(
        api_router,
        prefix="/api",
    )
    

    return app