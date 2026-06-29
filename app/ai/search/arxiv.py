import arxiv

from app.ai.shared.schemas import Paper
from app.ai.shared.exceptions import PaperSearchError


class ArxivSearchClient:
    """
    Client responsible for searching arXiv.
    """

    def __init__(self):

        self.client = arxiv.Client(
            page_size=5,
            delay_seconds=3,
            num_retries=3
        )


    async def search(
        self,
        query: str,
        limit: int = 5
    ) -> list[Paper]:

        try:

            search = arxiv.Search(
                query=f"all:{query}",
                max_results=limit,
                sort_by=arxiv.SortCriterion.Relevance
            )


            papers = []


            # Convert iterator safely
            results = list(
                self.client.results(search)
            )


            for item in results:

                papers.append(

                    Paper(

                        paper_id=item.entry_id,

                        title=item.title,

                        authors=[
                            author.name
                            for author in item.authors
                        ],

                        abstract=item.summary,

                        year=item.published.year,

                        pdf_url=item.pdf_url,

                        paper_url=item.entry_id,

                        source="arxiv"

                    )
                )


            return papers


        except Exception as e:

            raise PaperSearchError(
                f"arXiv search failed: {e}"
            )