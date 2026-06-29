import time
import inspect

from langgraph.graph import StateGraph, END

from app.core.logging import logger
from app.ai.workflows.state import ResearchState

# Workflow Nodes
from app.ai.workflows.nodes.planner import planner_node
from app.ai.workflows.nodes.paper_search import paper_search_node
from app.ai.workflows.nodes.pdf_download import pdf_download_node
from app.ai.workflows.nodes.document_processing import document_processing_node
from app.ai.workflows.nodes.embedding_generation import embedding_generation_node
from app.ai.workflows.nodes.vector_index import vector_index_node
from app.ai.workflows.nodes.retrieval import retrieval_node
from app.ai.workflows.nodes.rerank import rerank_node
from app.ai.workflows.nodes.context_builder import context_builder_node
from app.ai.workflows.nodes.answer_generation import answer_generation_node
from app.ai.workflows.nodes.citation_generation import citation_generation_node
from app.ai.workflows.nodes.report_generation import report_generation_node


def timed_node(name: str, node_func):
    """
    Logs execution time for both synchronous and asynchronous LangGraph nodes.
    """

    async def wrapper(state):

        logger.info("=" * 80)
        logger.info(f"START NODE : {name}")

        start = time.perf_counter()

        try:

            if inspect.iscoroutinefunction(node_func):
                result = await node_func(state)
            else:
                result = node_func(state)

            elapsed = time.perf_counter() - start

            logger.info(f"END NODE   : {name}")
            logger.info(f"TIME       : {elapsed:.2f} seconds")
            logger.info("=" * 80)

            return result

        except Exception:

            elapsed = time.perf_counter() - start

            logger.exception(
                f"ERROR in node '{name}' after {elapsed:.2f} seconds"
            )

            raise

    return wrapper


workflow = StateGraph(ResearchState)

# ============================================================================
# Register Nodes
# ============================================================================

workflow.add_node(
    "planner",
    timed_node("planner", planner_node),
)

workflow.add_node(
    "paper_search",
    timed_node("paper_search", paper_search_node),
)

workflow.add_node(
    "pdf_download",
    timed_node("pdf_download", pdf_download_node),
)

workflow.add_node(
    "document_processing",
    timed_node(
        "document_processing",
        document_processing_node,
    ),
)

workflow.add_node(
    "embedding_generation",
    timed_node(
        "embedding_generation",
        embedding_generation_node,
    ),
)

workflow.add_node(
    "vector_index",
    timed_node(
        "vector_index",
        vector_index_node,
    ),
)

workflow.add_node(
    "retrieval",
    timed_node(
        "retrieval",
        retrieval_node,
    ),
)

workflow.add_node(
    "rerank",
    timed_node(
        "rerank",
        rerank_node,
    ),
)

workflow.add_node(
    "context_builder",
    timed_node(
        "context_builder",
        context_builder_node,
    ),
)

workflow.add_node(
    "answer_generation",
    timed_node(
        "answer_generation",
        answer_generation_node,
    ),
)

workflow.add_node(
    "citation_generation",
    timed_node(
        "citation_generation",
        citation_generation_node,
    ),
)

workflow.add_node(
    "report_generation",
    timed_node(
        "report_generation",
        report_generation_node,
    ),
)

# ============================================================================
# Entry Point
# ============================================================================

workflow.set_entry_point("planner")

# ============================================================================
# Workflow Edges
# ============================================================================

workflow.add_edge(
    "planner",
    "paper_search",
)

workflow.add_edge(
    "paper_search",
    "pdf_download",
)

workflow.add_edge(
    "pdf_download",
    "document_processing",
)

workflow.add_edge(
    "document_processing",
    "embedding_generation",
)

workflow.add_edge(
    "embedding_generation",
    "vector_index",
)

workflow.add_edge(
    "vector_index",
    "retrieval",
)

workflow.add_edge(
    "retrieval",
    "rerank",
)

workflow.add_edge(
    "rerank",
    "context_builder",
)

workflow.add_edge(
    "context_builder",
    "answer_generation",
)

workflow.add_edge(
    "answer_generation",
    "citation_generation",
)

workflow.add_edge(
    "citation_generation",
    "report_generation",
)

workflow.add_edge(
    "report_generation",
    END,
)

research_graph = workflow.compile()