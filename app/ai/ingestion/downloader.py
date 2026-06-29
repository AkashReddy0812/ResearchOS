import os
import uuid

import httpx


from app.ai.shared.exceptions import PaperDownloadError
from app.ai.shared.schemas import Paper
from app.ai.ingestion.document import Document



class PDFDownloader:
    """
    Downloads research papers.
    """


    def __init__(
        self,
        storage_dir: str = "storage/papers"
    ):

        self.storage_dir = storage_dir

        os.makedirs(
            self.storage_dir,
            exist_ok=True
        )



    async def download(
        self,
        paper: Paper
    ) -> Document:


        if not paper.pdf_url:

            raise PaperDownloadError(
                "Paper does not contain PDF URL"
            )


        try:

            async with httpx.AsyncClient(
                timeout=30
            ) as client:


                response = await client.get(
                    paper.pdf_url
                )


                response.raise_for_status()


            filename = (
                f"{uuid.uuid4()}.pdf"
            )


            filepath = os.path.join(
                self.storage_dir,
                filename
            )


            with open(
                filepath,
                "wb"
            ) as f:

                f.write(
                    response.content
                )



            return Document(

                paper_id=paper.paper_id,

                title=paper.title,

                file_path=filepath,

                source_url=paper.pdf_url

            )


        except Exception as e:

            raise PaperDownloadError(
                f"PDF download failed: {e}"
            )