import httpx

from app.ai.shared.schemas import Paper
from app.ai.shared.exceptions import PaperSearchError


class SemanticScholarClient:

    BASE_URL = (
        "https://api.semanticscholar.org/graph/v1/paper/search"
    )


    async def search(
        self,
        query: str,
        limit: int = 5
    ) -> list[Paper]:

        params = {
            "query": query,
            "limit": limit,
            "fields":
            "title,abstract,authors,year,doi,url,openAccessPdf"
        }


        try:

            async with httpx.AsyncClient() as client:

                response = await client.get(
                    self.BASE_URL,
                    params=params
                )


            data = response.json()


            papers = []


            for item in data.get("data", []):

                papers.append(
                    Paper(

                        paper_id=item["paperId"],

                        title=item.get(
                            "title",
                            ""
                        ),

                        authors=[
                            a["name"]
                            for a in item.get(
                                "authors",
                                []
                            )
                        ],

                        abstract=item.get(
                            "abstract",
                            ""
                        ),

                        year=item.get("year"),

                        doi=item.get("doi"),

                        paper_url=item.get("url"),

                        pdf_url=(
                            item
                            .get(
                              "openAccessPdf",
                              {}
                            )
                            .get("url")
                        ),

                        source="semantic_scholar"
                    )
                )


            return papers


        except Exception as e:

            raise PaperSearchError(
                f"Semantic Scholar failed: {e}"
            )