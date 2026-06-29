import chromadb

from app.ai.shared.schemas import (
    EmbeddedChunk,
    VectorSearchResult
)


class ChromaVectorStore:
    """
    Vector database abstraction.
    """

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="storage/chroma"
        )


        self.collection = (
            self.client
            .get_or_create_collection(
                name="research_chunks"
            )
        )



    def add_chunks(
        self,
        chunks: list[EmbeddedChunk]
    ):

        ids = []
        documents = []
        embeddings = []
        metadatas = []


        for item in chunks:

            ids.append(
                item.chunk.chunk_id
            )

            documents.append(
                item.chunk.text
            )

            embeddings.append(
                item.embedding
            )


            metadatas.append(
                {
                    "paper_id":
                    item.chunk.paper_id
                }
            )


        self.collection.add(

            ids=ids,

            documents=documents,

            embeddings=embeddings,

            metadatas=metadatas
        )



    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5
    ) -> list[VectorSearchResult]:


        result = (
            self.collection
            .query(

                query_embeddings=[
                    query_embedding
                ],

                n_results=top_k

            )
        )


        output = []


        for i in range(
            len(result["ids"][0])
        ):

            output.append(

                VectorSearchResult(

                    chunk_id=
                    result["ids"][0][i],

                    paper_id=
                    result["metadatas"][0][i]
                    ["paper_id"],

                    text=
                    result["documents"][0][i],

                    score=
                    result["distances"][0][i]

                )

            )


        return output