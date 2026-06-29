class PromptBuilder:

    def build_research_prompt(

        self,

        query: str,

        context: str,

    ) -> str:

        return f"""
You are ResearchOS.

Answer ONLY using the provided context.

If evidence is insufficient,
say so.

Question:

{query}


Context:

{context}


Answer:
"""