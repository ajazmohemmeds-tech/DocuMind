import logging
from typing import List, Protocol, Union, Optional
from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_core.documents import Document
from api.core.config import settings
from retrieval.retrieval_service import EmbeddingService

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentLoader(Protocol):
    """Protocol for document loading services."""
    def load(self, source: Union[str, Path]) -> List[Document]:
        """Loads documents from a source."""
        ...

class PDFLoaderService:
    """PDF specific document loader service (using PyMuPDF for speed)."""
    def load(self, source: Union[str, Path]) -> List[Document]:
        """Loads a PDF document and splits it into pages."""
        loader = PyMuPDFLoader(str(source))
        return loader.load()

class URLBaseLoaderService:
    """Generic web document loader service."""
    def load(self, source: str) -> List[Document]:
        """Loads a document from a URL."""
        loader = WebBaseLoader(source)
        return loader.load()

class ChunkingService:
    """Service for chunking text from documents with optional SemanticChunker."""
    def __init__(self, mode: str = settings.CHUNKER_MODE):
        """Initializes the chunking service."""
        self.mode = mode
        if mode == "semantic":
            # Semantic chunking requires the embedding model
            embedding_service = EmbeddingService()
            self.text_splitter = SemanticChunker(embedding_service.get_embeddings())
        else:
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP,
                add_start_index=True
            )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Splits a list of documents into chunks."""
        logger.info(f"Chunking {len(documents)} docs using mode: {self.mode}")
        return self.text_splitter.split_documents(documents)

class IngestionService:
    """Orchestrates the ingestion pipeline (Phase 2)."""
    def __init__(self, chunker_mode: Optional[str] = None):
        """Initializes the ingestion service."""
        self.chunker = ChunkingService(mode=chunker_mode or settings.CHUNKER_MODE)
        self.pdf_loader = PDFLoaderService()
        self.url_loader = URLBaseLoaderService()

    def process_pdf(self, file_path: Union[str, Path]) -> List[Document]:
        """Processes a PDF file into chunks."""
        logger.info(f"Ingesting PDF: {file_path}")
        docs = self.pdf_loader.load(file_path)
        return self.chunker.split_documents(docs)

    def process_url(self, url: str) -> List[Document]:
        """Processes a URL into chunks."""
        logger.info(f"Ingesting URL: {url}")
        docs = self.url_loader.load(url)
        return self.chunker.split_documents(docs)
