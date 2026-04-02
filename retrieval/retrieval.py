import logging
import os
from typing import List, Optional, Union
from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers.ensemble import EnsembleRetriever
from langchain_core.documents import Document
from api.core.config import settings

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service for handling swappable embeddings (OpenAI or Local)."""
    def __init__(self):
        """Initializes the embedding service based on settings."""
        if settings.EMBEDDING_TYPE == "openai":
            logger.info(f"Using OpenAI Embeddings: {settings.OPENAI_EMBEDDING_MODEL}")
            self.embeddings = OpenAIEmbeddings(model=settings.OPENAI_EMBEDDING_MODEL)
        else:
            logger.info(f"Using Local Embeddings: {settings.LOCAL_EMBEDDING_MODEL}")
            # encode_kwargs ensures embeddings are standardized
            from langchain_huggingface import HuggingFaceEmbeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name=settings.LOCAL_EMBEDDING_MODEL,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
    
    def get_embeddings(self):
        """Returns the configured embedding model."""
        return self.embeddings


class VectorStoreService:
    """Service for managing the FAISS vector store (Phase 3)."""
    def __init__(self, index_path: Union[str, Path] = settings.FAISS_STORE_PATH):
        """Initializes the vector store service."""
        self.index_path = Path(index_path)
        self.embedding_service = EmbeddingService()
        self._vector_store: Optional[FAISS] = None

    def _load_vector_store(self) -> Optional[FAISS]:
        """Loads the FAISS index from disk if it exists."""
        if (self.index_path / "index.faiss").exists():
            try:
                self._vector_store = FAISS.load_local(
                    str(self.index_path),
                    self.embedding_service.get_embeddings(),
                    allow_dangerous_deserialization=True
                )
                logger.info(f"Loaded FAISS index from {self.index_path}")
            except Exception as e:
                logger.error(f"Failed to load FAISS index: {e}")
        return self._vector_store

    def add_documents(self, documents: List[Document]):
        """Adds documents to the FAISS index and persists it."""
        if not self._vector_store:
            self._vector_store = FAISS.from_documents(
                documents, self.embedding_service.get_embeddings()
            )
        else:
            self._vector_store.add_documents(documents)
        
        # Persist the FAISS index
        self._vector_store.save_local(str(self.index_path))
        logger.info(f"Persisted FAISS index with {len(documents)} new chunks.")

    def get_retriever(self, search_kwargs: dict = {"k": 4}):
        """Returns a FAISS retriever (Simplified for Render)."""
        if not self._vector_store:
            self._load_vector_store()
            if not self._vector_store:
                raise ValueError("Vector store is not initialized. Add documents first.")

        return self._vector_store.as_retriever(search_kwargs=search_kwargs)
