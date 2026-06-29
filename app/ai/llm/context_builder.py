from app.ai.shared.schemas import RetrievalResult


class ContextBuilder:
    """
    Builds the LLM context from reranked chunks.
    """

    def build(
        self,
        chunks: list[RetrievalResult],
    ) -> str:

        sections = []

        for chunk in chunks:
            sections.append(chunk.text)

        return "\n\n".join(sections)