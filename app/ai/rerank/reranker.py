from sentence_transformers import CrossEncoder

from app.ai.shared.schemas import RetrievalResult



class Reranker:
    """
    Cross encoder based reranking.

    Takes retrieved candidates
    and returns better ordering.
    """



    def __init__(self):

        self.model = CrossEncoder(
            "BAAI/bge-reranker-v2-m3"
        )



    def rerank(
        self,
        query: str,
        documents: list[RetrievalResult],
        top_k: int = 5
    ):

        pairs = []


        for doc in documents:

            pairs.append(
                [
                    query,
                    doc.text
                ]
            )


        scores = self.model.predict(
            pairs
        )


        ranked = []


        for doc,score in zip(
            documents,
            scores
        ):

            ranked.append(

                RetrievalResult(

                    chunk_id=doc.chunk_id,

                    paper_id=doc.paper_id,

                    text=doc.text,

                    score=float(score),

                    source="reranked"

                )

            )


        ranked.sort(
            key=lambda x:x.score,
            reverse=True
        )


        return ranked[:top_k]