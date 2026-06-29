from app.ai.embeddings.embedding_service import (
    EmbeddingService
)

from app.ai.workflows.state import (
    ResearchState
)

embedder = EmbeddingService()


def embedding_generation_node(
    state: ResearchState,
) -> ResearchState:

    embeddings = embedder.embed_chunks(
        state["chunks"]
    )

    state["embeddings"] = embeddings

    return state