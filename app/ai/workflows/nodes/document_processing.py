from app.ai.workflows.state import ResearchState

from app.ai.processing.parser import PDFParser
from app.ai.processing.cleaner import TextCleaner
from app.ai.processing.chunker import TextChunker


parser = PDFParser()

cleaner = TextCleaner()

chunker = TextChunker()



async def document_processing_node(
    state: ResearchState
) -> ResearchState:
    """
    Parse PDFs, clean text,
    generate chunks.
    """


    documents = []

    chunks = []


    for paper, pdf in zip(
        state["papers"],
        state["pdf_paths"]
    ):

        # await async parser
        document = await parser.parse(
            pdf
        )


        cleaned_text = cleaner.clean(
            document.text
        )


        paper_chunks = chunker.chunk(

            paper_id=paper.paper_id,

            text=cleaned_text

        )


        documents.append(
            cleaned_text
        )


        chunks.extend(
            paper_chunks
        )


    state["documents"] = documents

    state["chunks"] = chunks


    return state