from app.ai.workflows.state import ResearchState


def planner_node(state: ResearchState) -> ResearchState:
    """
    Initialize the workflow state and validate the user query.
    """

    query = state.get("query", "").strip()

    if not query:
        raise ValueError("Research query cannot be empty.")

    state.setdefault("papers", [])
    state.setdefault("pdf_paths", [])
    state.setdefault("documents", [])
    state.setdefault("chunks", [])
    state.setdefault("embeddings", [])
    state.setdefault("retrieved_chunks", [])
    state.setdefault("reranked_chunks", [])
    state.setdefault("context", "")
    state.setdefault("answer", "")
    state.setdefault("citations", [])
    state.setdefault("report", "")
    state.setdefault("errors", [])

    return state