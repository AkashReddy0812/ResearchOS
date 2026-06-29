from app.ai.reports.citation_service import CitationService

from app.ai.workflows.state import ResearchState



citation_service = CitationService()



def citation_generation_node(
    state: ResearchState
) -> ResearchState:


    citations = citation_service.generate(
        state["papers"]
    )


    state["citations"] = citations


    return state