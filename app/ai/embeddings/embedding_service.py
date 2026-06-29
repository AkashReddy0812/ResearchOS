from sentence_transformers import SentenceTransformer

from app.ai.shared.schemas import (
    Chunk,
    EmbeddedChunk
)

from app.ai.shared.config import ai_config

from app.ai.shared.exceptions import EmbeddingError



class EmbeddingService:
    """
    Generates vector embeddings.
    """



    def __init__(self):

        self.model = SentenceTransformer(
            ai_config.embedding_model
        )



    def embed_text(
        self,
        text: str
    ) -> list[float]:

        try:

            embedding = self.model.encode(
                text,
                normalize_embeddings=True
            )


            return embedding.tolist()


        except Exception as e:

            raise EmbeddingError(
                f"Embedding failed: {e}"
            )



    def embed_chunks(
        self,
        chunks: list[Chunk]
    ) -> list[EmbeddedChunk]:


        results = []


        texts = [
            chunk.text
            for chunk in chunks
        ]


        try:

            embeddings = self.model.encode(
                texts,
                normalize_embeddings=True
            )


            for chunk, vector in zip(
                chunks,
                embeddings
            ):

                results.append(
                    EmbeddedChunk(

                        chunk=chunk,

                        embedding=vector.tolist()

                    )
                )


            return results


        except Exception as e:

            raise EmbeddingError(
                f"Batch embedding failed: {e}"
            )