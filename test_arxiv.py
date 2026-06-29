import asyncio

from app.ai.search.arxiv import ArxivSearchClient


async def main():

    client = ArxivSearchClient()

    papers = await client.search(
        "transformer",
        limit=2
    )

    for p in papers:
        print(p.title)


asyncio.run(main())