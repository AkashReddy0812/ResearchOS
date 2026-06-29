class MarkdownReportGenerator:
    """
    Creates markdown research reports.
    """


    def generate(
        self,
        query: str,
        answer: str,
        citations: list[str]
    ) -> str:


        references = "\n".join(
            [
                f"- {c}"
                for c in citations
            ]
        )


        report = f"""

# ResearchOS Report


## Query

{query}


## Answer

{answer}


## References

{references}

"""


        return report