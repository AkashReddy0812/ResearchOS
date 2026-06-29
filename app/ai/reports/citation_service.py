from app.ai.shared.schemas import Citation, Paper


class CitationService:
    """
    Generates structured citations from research papers.

    Future:
    - APA
    - MLA
    - IEEE
    - BibTeX
    """

    def generate(
        self,
        papers: list[Paper],
    ) -> list[Citation]:

        citations = []

        for paper in papers:

            citations.append(
                Citation(
                    title=paper.title,
                    authors=paper.authors,
                    year=paper.year,
                    source=paper.paper_url or paper.pdf_url or paper.source,
                    doi=paper.doi,
                )
            )

        return citations