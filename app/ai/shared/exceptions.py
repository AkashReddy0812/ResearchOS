"""
Custom exceptions used throughout the AI pipeline.
"""


class AIException(Exception):
    """Base class for all AI exceptions."""


class PaperSearchError(AIException):
    """Raised when searching research papers fails."""


class PaperDownloadError(AIException):
    """Raised when downloading a paper fails."""


class DocumentProcessingError(AIException):
    """Raised when parsing or chunking fails."""


class EmbeddingError(AIException):
    """Raised when embedding generation fails."""


class VectorStoreError(AIException):
    """Raised when vector database operations fail."""


class RetrievalError(AIException):
    """Raised during retrieval."""


class RerankError(AIException):
    """Raised during reranking."""


class LLMGenerationError(AIException):
    """Raised when the LLM fails."""