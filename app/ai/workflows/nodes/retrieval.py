from app.ai.retrieval.hybrid_retriever import (
    HybridRetriever
)

from app.ai.workflows.state import (
    ResearchState
)

retriever = HybridRetriever()


def retrieval_node(
    state: ResearchState,
) -> ResearchState:

    chunks = retriever.retrieve(

        query=state["query"]

    )

    state["retrieved_chunks"] = chunks

    return state