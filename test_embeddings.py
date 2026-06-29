import asyncio


from app.ai.search.search_service import SearchService
from app.ai.ingestion.downloader import PDFDownloader

from app.ai.processing.parser import PDFParser
from app.ai.processing.cleaner import TextCleaner
from app.ai.processing.chunker import TextChunker

from app.ai.embeddings.embedding_service import EmbeddingService



async def main():

    search = SearchService()


    papers = await search.search(
        "large language models"
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


    text = cleaner.clean(
        parsed.text
    )


    chunker = TextChunker()


    chunks = chunker.chunk(
        parsed.paper_id,
        text
    )


    service = EmbeddingService()


    embedded = service.embed_chunks(
        chunks[:3]
    )


    print(
        "Chunks embedded:",
        len(embedded)
    )


    print(
        "Vector size:",
        len(
            embedded[0].embedding
        )
    )



asyncio.run(main())