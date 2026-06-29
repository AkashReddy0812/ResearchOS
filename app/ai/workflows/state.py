from typing_extensions import TypedDict

from app.ai.shared.schemas import (
    Paper,
    Chunk,
    EmbeddedChunk,
    VectorSearchResult,
)


class ResearchState(TypedDict):
    """
    Shared state flowing through the LangGraph
    research workflow.
    """

    # ==========================
    # User Query
    # ==========================
    query: str

    # ==========================
    # Search
    # ==========================
    papers: list[Paper]

    # ==========================
    # PDF Download
    # ==========================
    pdf_paths: list[str]

    # ==========================
    # Document Processing
    # ==========================
    documents: list[str]

    chunks: list[Chunk]

    # ==========================
    # Embeddings
    # ==========================
    embeddings: list[EmbeddedChunk]

    # ==========================
    # Retrieval
    # ==========================
    retrieved_chunks: list[VectorSearchResult]

    reranked_chunks: list[VectorSearchResult]

    # ==========================
    # LLM
    # ==========================
    context: str

    answer: str

    # ==========================
    # Output
    # ==========================
    citations: list[str]

    report: str

    # ==========================
    # Errors
    # ==========================
    errors: list[str]