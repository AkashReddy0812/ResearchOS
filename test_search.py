import asyncio

from app.ai.search.search_service import SearchService


async def main():

    service = SearchService()

    papers = await service.search(
        "retrieval augmented generation"
    )


    print(
        f"\nFound {len(papers)} papers"
    )


    for i, paper in enumerate(papers,1):

        print("\n====================")
        print("Paper:", i)
        print("Title:", paper.title)
        print("Authors:", paper.authors[:3])
        print("Year:", paper.year)
        print("Source:", paper.source)

        print(
            "PDF:",
            paper.pdf_url
        )


asyncio.run(main())