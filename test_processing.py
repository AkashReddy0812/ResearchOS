import asyncio


from app.ai.search.search_service import SearchService
from app.ai.ingestion.downloader import PDFDownloader

from app.ai.processing.parser import PDFParser
from app.ai.processing.cleaner import TextCleaner
from app.ai.processing.chunker import TextChunker



async def main():

    search = SearchService()

    papers = await search.search(
        "transformer architecture"
    )


    downloader = PDFDownloader()


    document = await downloader.download(
        papers[0]
    )


    parser = PDFParser()


    parsed = await parser.parse(
        document
    )


    cleaner = TextCleaner()


    clean_text = cleaner.clean(
        parsed.text
    )


    chunker = TextChunker()


    chunks = chunker.chunk(
        parsed.paper_id,
        clean_text
    )


    print(
        "Pages:",
        parsed.pages
    )


    print(
        "Chunks:",
        len(chunks)
    )


    print(
        chunks[0].text[:300]
    )



asyncio.run(main())