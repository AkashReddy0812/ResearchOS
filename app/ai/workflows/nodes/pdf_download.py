from app.ai.ingestion.downloader import PDFDownloader

from app.ai.workflows.state import ResearchState



downloader = PDFDownloader()



async def pdf_download_node(
    state: ResearchState
) -> ResearchState:
    """
    Download paper PDFs.
    """


    pdf_paths = []


    for paper in state["papers"]:

        path = await downloader.download(
            paper
        )

        pdf_paths.append(
            path
        )


    state["pdf_paths"] = pdf_paths


    return state