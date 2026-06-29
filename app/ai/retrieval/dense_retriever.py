from app.ai.vectorstore.chroma_service import ChromaVectorStore
from app.ai.embeddings.embedding_service import EmbeddingService

from app.ai.shared.schemas import RetrievalResult



class DenseRetriever:
    """
    Semantic vector retrieval.
    """


    def __init__(self):

        self.vectorstore = ChromaVectorStore()

        self.embedder = EmbeddingService()



    def retrieve(
        self,
        query: str,
        top_k: int = 10
    ) -> list[RetrievalResult]:


        query_embedding = (
            self.embedder.embed_text(
                query
            )
        )


        results = self.vectorstore.search(
            query_embedding,
            top_k
        )


        return [

            RetrievalResult(

                chunk_id=r.chunk_id,

                paper_id=r.paper_id,

                text=r.text,

                score=r.score,

                source="dense"

            )

            for r in results

        ]