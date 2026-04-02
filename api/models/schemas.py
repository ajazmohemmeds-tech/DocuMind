from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class URLUploadRequest(BaseModel):
    """Request model for URL ingestion."""
    url: str

class QueryRequest(BaseModel):
    """Request model for document queries."""
    query: str

class SourceCitation(BaseModel):
    """Citation metadata entry."""
    page_content: str
    metadata: Dict[str, Any]

class QueryResponse(BaseModel):
    """Response model for document queries."""
    answer: str
    sources: List[SourceCitation]

class ChunkInfo(BaseModel):
    """Information about a single text chunk."""
    page_content: str
    metadata: Dict[str, Any]

class DocumentChunksResponse(BaseModel):
    """Response model for document chunks."""
    doc_id: str
    chunks: List[ChunkInfo]
