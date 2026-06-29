from app.ai.llm.prompt_builder import PromptBuilder


class Generator:
    """
    LLM generation service.

    Keeps model interaction isolated
    from LangGraph and API layers.
    """

    def __init__(self):
        self.prompt_builder = PromptBuilder()


    def generate(
        self,
        query: str,
        context: str
    ) -> str:

        prompt = self.prompt_builder.build_research_prompt(
            query=query,
            context=context
        )


        # MVP placeholder
        # Replace with OpenAI / Anthropic / Ollama later

        answer = (
            "Research Answer\n\n"
            f"Question:\n{query}\n\n"
            "Based on retrieved papers:\n\n"
            f"{context[:2000]}"
        )


        return answer