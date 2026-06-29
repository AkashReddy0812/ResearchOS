from rank_bm25 import BM25Okapi

from app.ai.shared.schemas import RetrievalResult



class BM25Retriever:
    """
    Keyword based retrieval.
    """



    def __init__(
        self,
        documents: list[RetrievalResult]
    ):

        self.documents = documents


        corpus = [

            doc.text.split()

            for doc in documents

        ]


        self.bm25 = BM25Okapi(
            corpus
        )



    def retrieve(
        self,
        query: str,
        top_k: int = 10
    ) -> list[RetrievalResult]:


        tokens = query.split()


        scores = self.bm25.get_scores(
            tokens
        )


        ranked = sorted(

            zip(
                self.documents,
                scores
            ),

            key=lambda x:x[1],

            reverse=True

        )


        return [

            RetrievalResult(

                chunk_id=doc.chunk_id,

                paper_id=doc.paper_id,

                text=doc.text,

                score=float(score),

                source="bm25"

            )

            for doc,score in ranked[:top_k]

        ]