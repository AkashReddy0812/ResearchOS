import asyncio


from app.ai.search.search_service import SearchService
from app.ai.ingestion.downloader import PDFDownloader

from app.ai.processing.parser import PDFParser
from app.ai.processing.cleaner import TextCleaner
from app.ai.processing.chunker import TextChunker

from app.ai.embeddings.embedding_service import EmbeddingService

from app.ai.vectorstore.chroma_service import ChromaVectorStore



async def main():


    search = SearchService()


    papers = await search.search(
        "attention mechanism transformers"
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


    embedder = EmbeddingService()


    embedded = embedder.embed_chunks(
        chunks[:10]
    )


    db = ChromaVectorStore()


    db.add_chunks(
        embedded
    )


    query_vector = (
        embedder.embed_text(
            "attention mechanism"
        )
    )


    results = db.search(
        query_vector
    )


    for r in results:

        print(
            "\nScore:",
            r.score
        )

        print(
            r.text[:200]
        )



asyncio.run(main())