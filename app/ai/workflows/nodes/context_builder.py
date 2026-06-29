from app.ai.llm.context_builder import ContextBuilder
from app.ai.workflows.state import ResearchState


builder = ContextBuilder()


def context_builder_node(
    state: ResearchState,
) -> ResearchState:
    """
    LangGraph node that builds the LLM context.
    """

    state["context"] = builder.build(
        state["reranked_chunks"]
    )

    return state