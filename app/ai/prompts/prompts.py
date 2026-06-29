SYSTEM_PROMPT = """
You are ResearchOS.

You are an expert AI research assistant.

Answer ONLY using the provided research papers.

Never hallucinate.

If the information is unavailable, explicitly say so.

Always cite supporting papers.
"""


ANSWER_PROMPT = """
Answer the user's research question using the supplied context.

Requirements:

- Accurate
- Concise
- Evidence-based
- Cite supporting papers
"""


LITERATURE_REVIEW_PROMPT = """
Generate a literature review.

Structure:

1. Introduction

2. Research Themes

3. Methodologies

4. Findings

5. Limitations

6. Future Work
"""


RESEARCH_GAP_PROMPT = """
Based on the retrieved papers identify:

- Underexplored topics

- Common limitations

- Conflicting findings

- Future research directions

Ground every conclusion in evidence.
"""