import fitz


from app.ai.ingestion.document import Document
from app.ai.shared.schemas import ParsedDocument
from app.ai.shared.exceptions import DocumentProcessingError



class PDFParser:
    """
    Extracts text from PDFs.
    """



    async def parse(
        self,
        document: Document
    ) -> ParsedDocument:


        try:

            pdf = fitz.open(
                document.file_path
            )


            pages = []


            for page in pdf:

                text = page.get_text()

                pages.append(text)



            full_text = "\n".join(
                pages
            )


            return ParsedDocument(

                paper_id=document.paper_id,

                title=document.title,

                text=full_text,

                pages=len(pdf)

            )


        except Exception as e:

            raise DocumentProcessingError(
                f"PDF parsing failed: {e}"
            )