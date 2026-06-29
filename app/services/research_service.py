from app.ai.shared.schemas import ResearchResponse
from app.ai.workflows.graph import research_graph


class ResearchService:
    """
    Main entry point for all AI-related operations.

    Responsibilities:
    - Create the initial workflow state.
    - Execute the LangGraph workflow.
    - Convert the workflow output into a ResearchResponse.
    """

    async def research(
        self,
        query: str,
    ) -> ResearchResponse:
        """
        Executes the complete ResearchOS workflow.
        """

        initial_state = {
            "query": query,

            "papers": [],
            "pdf_paths": [],
            "documents": [],
            "chunks": [],
            "embeddings": [],
            "retrieved_chunks": [],
            "reranked_chunks": [],

            "context": "",
            "answer": "",

            "citations": [],

            "report": "",

            "errors": [],
        }

        result = await research_graph.ainvoke(initial_state)

        return ResearchResponse(
            answer=result.get("answer", ""),

            citations=result.get("citations", []),

            retrieved_papers=result.get("papers", []),
        )