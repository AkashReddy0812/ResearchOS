import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Adds a unique request ID and processing time to each request.
    """

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())

        start_time = time.perf_counter()

        request.state.request_id = request_id

        response = await call_next(request)

        duration = time.perf_counter() - start_time

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{duration:.4f}"

        return response