from typing import List, Optional

from pydantic import BaseModel, Field


class Paper(BaseModel):
    """
    Unified representation of a research paper.
    """

    paper_id: str

    title: str

    authors: List[str] = Field(default_factory=list)

    abstract: str = ""

    year: Optional[int] = None

    doi: Optional[str] = None

    pdf_url: Optional[str] = None

    paper_url: Optional[str] = None

    source: str


class ParsedDocument(BaseModel):
    """
    Extracted text from a document.
    """

    paper_id: str

    title: str

    text: str

    pages: int


class Chunk(BaseModel):
    """
    One chunk of a processed paper.
    """

    chunk_id: str

    paper_id: str

    text: str

    page: Optional[int] = None

    section: Optional[str] = None


class RetrievedChunk(BaseModel):
    """
    Chunk returned from retrieval.
    """

    chunk: Chunk

    score: float

    retrieval_method: str

class EmbeddedChunk(BaseModel):
    """
    Chunk with generated embedding.
    """

    chunk: Chunk

    embedding: list[float]

class VectorSearchResult(BaseModel):
    """
    Result returned from vector database.
    """

    chunk_id: str

    paper_id: str

    text: str

    score: float

class RetrievalResult(BaseModel):
    """
    Common retrieval output.
    """

    chunk_id: str

    paper_id: str

    text: str

    score: float

    source: str



class Citation(BaseModel):
    title: str

    authors: List[str]

    year: Optional[int]

    source: str

    doi: Optional[str]


class ResearchResponse(BaseModel):
    """
    Final response returned by ResearchOS.
    """

    answer: str

    literature_review: Optional[str] = None

    research_gaps: Optional[str] = None

    citations: List[Citation] = Field(default_factory=list)

    retrieved_papers: List[Paper] = Field(default_factory=list)