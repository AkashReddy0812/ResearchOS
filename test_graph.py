import asyncio


from app.ai.workflows.graph import (
    research_graph
)



async def main():


    result = await research_graph.ainvoke(

        {
            "query":
            "transformer attention",

            "papers":[],
            "documents":[],
            "retrieved_chunks":[],
            "reranked_chunks":[],
            "answer":"",
            "report":""

        }

    )


    print(
        result["answer"]
    )



asyncio.run(main())