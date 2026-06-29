from app.ai.search.arxiv import ArxivSearchClient
from app.ai.search.semantic_scholar import SemanticScholarClient

from app.ai.shared.schemas import Paper


class SearchService:
    """
    Aggregates multiple research sources.
    """


    def __init__(self):

        self.arxiv = ArxivSearchClient()

        self.semantic = SemanticScholarClient()



    async def search(
        self,
        query: str
    ) -> list[Paper]:


        arxiv_results = await self.arxiv.search(
            query
        )


        semantic_results = await self.semantic.search(
            query
        )


        combined = (
            arxiv_results
            +
            semantic_results
        )


        return self._deduplicate(
            combined
        )


    def _deduplicate(
        self,
        papers: list[Paper]
    ) -> list[Paper]:

        seen = set()

        unique = []


        for paper in papers:

            key = (
                paper.title
                .lower()
                .strip()
            )


            if key not in seen:

                seen.add(key)

                unique.append(
                    paper
                )


        return unique