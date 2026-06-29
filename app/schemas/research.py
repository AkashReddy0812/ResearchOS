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