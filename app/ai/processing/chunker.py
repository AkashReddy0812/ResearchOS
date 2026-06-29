from app.ai.shared.config import ai_config
from app.ai.shared.schemas import Chunk


import uuid



class TextChunker:
    """
    Splits documents into RAG chunks.
    """



    def chunk(
        self,
        paper_id: str,
        text: str
    ) -> list[Chunk]:


        size = ai_config.chunk_size

        overlap = ai_config.chunk_overlap


        chunks = []


        start = 0


        while start < len(text):

            end = start + size


            chunk_text = text[start:end]


            chunks.append(
                Chunk(

                    chunk_id=str(
                        uuid.uuid4()
                    ),

                    paper_id=paper_id,

                    text=chunk_text

                )
            )


            start = (
                end - overlap
            )


        return chunks