import pickle

from rank_bm25 import BM25Okapi



class BM25Store:


    def __init__(self):

        self.model = None
        self.documents = []



    def build(
        self,
        documents: list[str]
    ):

        self.documents = documents


        tokenized = [
            doc.split()
            for doc in documents
        ]


        self.model = BM25Okapi(
            tokenized
        )



    def search(
        self,
        query: str,
        top_k: int = 10
    ):

        scores = self.model.get_scores(
            query.split()
        )


        ranked = sorted(
            enumerate(scores),
            key=lambda x:x[1],
            reverse=True
        )


        return [
            {
                "index":idx,
                "score":score
            }

            for idx,score in ranked[:top_k]
        ]