from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: str
    details: Any | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)