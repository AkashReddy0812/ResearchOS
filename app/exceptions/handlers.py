from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import ResearchOSError
from app.schemas.response import ErrorResponse


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(ResearchOSError)
    async def researchos_exception_handler(
        request: Request,
        exc: ResearchOSError,
    ):
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(
                message=exc.message,
                error_code=exc.error_code,
            ).model_dump(mode="json"),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ):
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                message="Internal Server Error",
                error_code="INTERNAL_SERVER_ERROR",
            ).model_dump(mode="json"),
        )