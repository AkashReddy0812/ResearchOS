from app.ai.reports.markdown_report import (
    MarkdownReportGenerator
)

from app.ai.workflows.state import ResearchState



report_generator = MarkdownReportGenerator()



def report_generation_node(
    state: ResearchState
) -> ResearchState:


    report = report_generator.generate(

        query=state["query"],

        answer=state["answer"],

        citations=state["citations"]

    )


    state["report"] = report


    return state