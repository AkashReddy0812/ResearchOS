from pydantic import BaseModel, Field


class AIConfig(BaseModel):
    """
    Central configuration for the AI pipeline.
    """

    # ==========================
    # Search Configuration
    # ==========================

    max_search_results: int = Field(
        default=10,
        description="Maximum number of papers fetched from each provider.",
    )

    # ==========================
    # Document Processing
    # ==========================

    chunk_size: int = Field(
        default=1000,
        description="Maximum characters per chunk.",
    )

    chunk_overlap: int = Field(
        default=200,
        description="Overlap between consecutive chunks.",
    )

    # ==========================
    # Embedding
    # ==========================

    embedding_model: str = "BAAI/bge-m3"

    # ==========================
    # Vector Database
    # ==========================

    chroma_collection: str = "research_papers"

    # ==========================
    # Retrieval
    # ==========================

    dense_top_k: int = 20
    sparse_top_k: int = 20
    rerank_top_k: int = 8

    # ==========================
    # LLM
    # ==========================

    llm_model: str = "gemini-2.5-flash"

    temperature: float = 0.2


ai_config = AIConfig()