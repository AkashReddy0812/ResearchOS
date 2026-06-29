import asyncio

from app.ai.retrieval.hybrid_retriever import HybridRetriever



async def main():

    retriever = HybridRetriever()


    results = retriever.retrieve(
        "attention mechanism"
    )


    for r in results:

        print(
            "\n",
            r.source,
            r.score
        )

        print(
            r.text[:200]
        )


asyncio.run(main())