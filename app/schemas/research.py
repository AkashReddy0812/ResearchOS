from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=3,
        description="Research query to execute."
    )


class ResearchResponse(BaseModel):
    query: str
    answer: str
    citations: list[str]
    papers: list[dict]
    report: str
    errors: list[str]


class JobCreateResponse(BaseModel):
    job_id: str
    status: str


from datetime import datetime
from typing import Any

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    current_node: str | None
    iteration_count: int
    sufficiency_score: float
    coverage_metrics: dict[str, Any] | None
    updated_at: datetime