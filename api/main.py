import logging
import uuid
import shutil
import asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.responses import StreamingResponse
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware
from api.models.schemas import URLUploadRequest, QueryRequest, QueryResponse, DocumentChunksResponse, ChunkInfo
from ingestion.ingestion_service import IngestionService
from retrieval.retrieval_service import VectorStoreService
from retrieval.qa_service import ResearchService
from api.core.config import settings

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="DocuMind Research API", version="2.0.0 (Phase 5)")

# CORS Middleware for React Integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://localhost:5174", 
        "http://localhost:5175", 
        "http://localhost:5176",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ingestion_service = IngestionService()
vector_store_service = VectorStoreService()
qa_service = ResearchService()

@app.post("/upload/pdf", response_model=Dict[str, str])
async def upload_pdf(file: UploadFile = File(...)):
    """Uploads a PDF file using PyMuPDF (Phase 2)."""
    file_id = str(uuid.uuid4())
    file_path = settings.DATA_STORE_PATH / f"{file_id}.pdf"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        chunks = ingestion_service.process_pdf(file_path)
        vector_store_service.add_documents(chunks)
        return {"id": file_id, "message": f"PDF ingested with {len(chunks)} chunks."}
    except Exception as e:
        logger.error(f"PDF upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload/url", response_model=Dict[str, str])
async def upload_url(request: URLUploadRequest):
    """Processes a URL (Phase 2)."""
    try:
        chunks = ingestion_service.process_url(request.url)
        vector_store_service.add_documents(chunks)
        return {"id": request.url, "message": f"URL ingested with {len(chunks)} chunks."}
    except Exception as e:
        logger.error(f"URL upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_documents_stream(request: QueryRequest):
    """Refine Insights from documents (Phase 5)."""
    try:
        retriever = vector_store_service.get_retriever()
        qa_chain = qa_service.get_qa_chain(retriever)
        
        if not qa_chain:
             raise HTTPException(status_code=500, detail="QA service not initialized. Check API keys.")

        async def stream_generator():
            # Using invoke formally and splitting for the UI stream simulation
            response = await asyncio.to_thread(qa_chain.invoke, {"query": request.query})
            answer = response["result"]
            
            if not answer:
                yield "No insights found for this query."
                return

            for chunk in answer.split(" "):
                yield chunk + " "
                await asyncio.sleep(0.01)
        
        return StreamingResponse(stream_generator(), media_type="text/plain")
    except Exception as e:
        logger.error(f"Stream query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query/full", response_model=QueryResponse)
async def query_documents_full(request: QueryRequest):
    """Query documents without streaming (Standard)."""
    try:
        retriever = vector_store_service.get_retriever()
        response = qa_service.query(request.query, retriever)
        return QueryResponse(
            answer=response["answer"],
            sources=[{"page_content": s["page_content"], "metadata": s["metadata"]} for s in response["sources"]]
        )
    except Exception as e:
        logger.error(f"Full query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/clear")
async def clear_knowledge_base():
    """Clears the FAISS store (Phase 6)."""
    try:
        vector_store_service.clear_index()
        return {"message": "Knowledge base cleared successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
