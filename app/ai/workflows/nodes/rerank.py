from app.ai.rerank.reranker import (
    Reranker
)

from app.ai.workflows.state import (
    ResearchState
)

reranker = Reranker()


def rerank_node(
    state: ResearchState,
) -> ResearchState:

    chunks = reranker.rerank(

        query=state["query"],

        documents=state["retrieved_chunks"]

    )

    state["reranked_chunks"] = chunks

    return state