import asyncio

from app.ai.workflows.graph import research_graph


async def main():

    result = await research_graph.ainvoke(
        {
            "query": "transformer architecture in deep learning",

            "papers": [],
            "pdf_paths": [],
            "documents": [],
            "chunks": [],
            "embeddings": [],
            "retrieved_chunks": [],
            "reranked_chunks": [],
            "context": "",
            "answer": "",
            "citations": [],
            "report": "",
            "errors": [],
        }
    )


    print("\n\n========== ANSWER ==========\n")

    print(
        result["answer"]
    )


    print("\n\n========== CITATIONS ==========\n")

    for c in result["citations"]:
        print(c)


    print("\n\n========== REPORT ==========\n")

    print(
        result["report"]
    )



if __name__ == "__main__":

    asyncio.run(main())