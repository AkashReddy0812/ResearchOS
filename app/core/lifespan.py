from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logging import logger

from app.db.base import Base
from app.db.session import engine





@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle.
    """

    logger.info("Starting ResearchOS...")

    #
    # Future initialization:
    #
    # Database
    # Redis
    # Vector DB
    # AI Clients
    #


    import app.db.models  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


    yield

    logger.info("Shutting down ResearchOS...")

    #
    # Future cleanup
    #