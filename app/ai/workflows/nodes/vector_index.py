from app.ai.vectorstore.chroma_service import ChromaVectorStore
from app.ai.workflows.state import ResearchState


vector_store = ChromaVectorStore()


def vector_index_node(
    state: ResearchState,
) -> ResearchState:
    """
    Index embedded chunks into ChromaDB.
    """

    vector_store.add_chunks(
        state["embeddings"]
    )

    return state