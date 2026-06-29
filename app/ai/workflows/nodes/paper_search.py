from app.ai.search.search_service import SearchService
from app.ai.workflows.state import ResearchState

search_service = SearchService()


async def paper_search_node(
    state: ResearchState,
) -> ResearchState:
    """
    Search research papers.
    """

    papers = await search_service.search(
        state["query"]
    )

    state["papers"] = papers

    return state