from collections import defaultdict

from app.ai.shared.schemas import RetrievalResult



class ReciprocalRankFusion:
    """
    Combines multiple ranked lists.
    """



    def fuse(
        self,
        results: list[list[RetrievalResult]],
        k: int = 60
    ):

        scores = defaultdict(float)

        docs = {}


        for ranking in results:

            for rank,doc in enumerate(
                ranking,
                start=1
            ):

                scores[
                    doc.chunk_id
                ] += 1 / (
                    k + rank
                )


                docs[
                    doc.chunk_id
                ] = doc



        final = []


        for chunk_id,score in scores.items():

            doc = docs[chunk_id]


            final.append(

                RetrievalResult(

                    chunk_id=doc.chunk_id,

                    paper_id=doc.paper_id,

                    text=doc.text,

                    score=score,

                    source="rrf"

                )

            )


        return sorted(
            final,
            key=lambda x:x.score,
            reverse=True
        )