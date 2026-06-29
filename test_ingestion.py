import asyncio


from app.ai.search.search_service import SearchService
from app.ai.ingestion.downloader import PDFDownloader



async def main():

    search = SearchService()


    papers = await search.search(
        "retrieval augmented generation"
    )


    paper = papers[0]


    print(
        "Downloading:"
    )

    print(
        paper.title
    )


    downloader = PDFDownloader()


    document = await downloader.download(
        paper
    )


    print(
        "\nSaved:"
    )

    print(
        document.file_path
    )



asyncio.run(main())