from app.ai.retrieval.dense_retriever import DenseRetriever
from app.ai.retrieval.bm25_retriever import BM25Retriever
from app.ai.retrieval.rrf import ReciprocalRankFusion

from app.ai.shared.schemas import RetrievalResult



class HybridRetriever:
    """
    Hybrid Retrieval System.

    Combines:
    - Dense semantic search
    - Sparse keyword search

    using Reciprocal Rank Fusion.
    """



    def __init__(
        self,
        documents: list[RetrievalResult] = None
    ):

        self.dense = DenseRetriever()

        self.rrf = ReciprocalRankFusion()


        self.bm25 = None


        if documents:

            self.bm25 = BM25Retriever(
                documents
            )



    def retrieve(
        self,
        query: str,
        top_k: int = 10
    ) -> list[RetrievalResult]:


        #
        # Dense retrieval
        #
        dense_results = (
            self.dense.retrieve(
                query,
                top_k
            )
        )


        rankings = [
            dense_results
        ]



        #
        # Sparse retrieval
        #
        if self.bm25:


            bm25_results = (
                self.bm25.retrieve(
                    query,
                    top_k
                )
            )


            rankings.append(
                bm25_results
            )



        #
        # Reciprocal Rank Fusion
        #
        final_results = (
            self.rrf.fuse(
                rankings
            )
        )


        return final_results[:top_k]