import logging
from abc import ABC, abstractmethod
from typing import List, Protocol, Union, Optional
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from api.core.config import settings

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentLoader(Protocol):
    """Protocol for document loading services."""
    def load(self, source: Union[str, Path]) -> List[Document]:
        """Loads documents from a source."""
        ...

class PDFLoaderService:
    """PDF specific document loader service."""
    def load(self, source: Union[str, Path]) -> List[Document]:
        """Loads a PDF document and splits it into pages."""
        loader = PyPDFLoader(str(source))
        return loader.load()

class URLBaseLoaderService:
    """Generic web document loader service."""
    def load(self, source: str) -> List[Document]:
        """Loads a document from a URL."""
        loader = WebBaseLoader(source)
        return loader.load()

class ChunkingService:
    """Service for chunking text from documents."""
    def __init__(self, chunk_size: int = settings.CHUNK_SIZE, chunk_overlap: int = settings.CHUNK_OVERLAP):
        """Initializes the chunking service."""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            add_start_index=True
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Splits a list of documents into chunks."""
        return self.text_splitter.split_documents(documents)

class IngestionService:
    """Orchestrates the ingestion pipeline."""
    def __init__(self, chunk_size: Optional[int] = None, chunk_overlap: Optional[int] = None):
        """Initializes the ingestion service."""
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
        self.chunker = ChunkingService(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        self.pdf_loader = PDFLoaderService()
        self.url_loader = URLBaseLoaderService()

    def process_pdf(self, file_path: Union[str, Path]) -> List[Document]:
        """Processes a PDF file into chunks."""
        logger.info(f"Processing PDF: {file_path}")
        docs = self.pdf_loader.load(file_path)
        return self.chunker.split_documents(docs)

    def process_url(self, url: str) -> List[Document]:
        """Processes a URL into chunks."""
        logger.info(f"Processing URL: {url}")
        docs = self.url_loader.load(url)
        return self.chunker.split_documents(docs)
