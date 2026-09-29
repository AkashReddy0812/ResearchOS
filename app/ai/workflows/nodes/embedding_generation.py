from functools import lru_cache

from app.ai.embeddings.embedding_service import EmbeddingService
from app.ai.workflows.state import ResearchState


@lru_cache(maxsize=1)
def get_embedder():
    return EmbeddingService()


def embedding_generation_node(state: ResearchState) -> ResearchState:
    embedder = get_embedder()

    embeddings = embedder.embed_chunks(state["chunks"])

    state["embeddings"] = embeddings

    return state