import logging
# Lazy imports for providers handled in __init__
from typing import List, Dict, Any, Union
from langchain_core.documents import Document
from api.core.config import settings


# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResearchService:
    """Service for generating research insights with Swappable Providers (Simplified)."""
    def __init__(self):
        """Initializes the research service with support for multiple providers."""
        self.provider = settings.MODEL_PROVIDER.lower()
        self.model = None
        
        try:
            if self.provider == "google":
                from langchain_google_genai import ChatGoogleGenerativeAI
                self.model = ChatGoogleGenerativeAI(
                    model=settings.GOOGLE_MODEL,
                    google_api_key=settings.GOOGLE_API_KEY,
                    temperature=0
                )
            elif self.provider == "anthropic":
                from langchain_anthropic import ChatAnthropic
                self.model = ChatAnthropic(
                    model=settings.ANTHROPIC_MODEL,
                    anthropic_api_key=settings.ANTHROPIC_API_KEY,
                    temperature=0
                )
            else: # Default to OpenAI
                from langchain_openai import ChatOpenAI
                self.model = ChatOpenAI(
                    model=settings.OPENAI_MODEL,
                    openai_api_key=settings.OPENAI_API_KEY,
                    temperature=0
                )
            
            if self.model:
                logger.info(f"Initialized ResearchService with provider: {self.provider}")
        except Exception as e:
            logger.error(f"Failed to initialize {self.provider} model: {e}")
            self.model = None
        
        # Base prompt for the assistant
        self.system_prompt = """You are DocuMind, a precise and scholarly Research Assistant.
Synthesize the information below based ONLY on the provided context.
Include source citations (e.g., [Source 1], [Source 2]) in your response wherever appropriate.
If the context doesn't contain enough information to complete the inquiry, state that clearly."""

    def query(self, question: str, retriever) -> Dict[str, Any]:
        """Runs a manual query by retrieving docs and prompting the LLM."""
        if not self.model:
            return {
                "answer": f"Error: {self.provider.upper()}_API_KEY not configured.",
                "sources": []
            }
            
        try:
            # 1. Retrieve relevant documents
            docs = retriever.get_relevant_documents(question)
            
            # 2. Format context
            context = "\n\n".join([f"[Source {i+1}]: {doc.page_content}" for i, doc in enumerate(docs)])
            
            # 3. Create prompt
            prompt = f"{self.system_prompt}\n\nContext:\n{context}\n\nInquiry: {question}\n\nResponse with citations:"
            
            # 4. Call LLM
            response = self.model.invoke(prompt)
            answer = response.content if hasattr(response, 'content') else str(response)
            
            # 5. Extract sources
            sources = [
                {
                    "page_content": doc.page_content,
                    "metadata": doc.metadata
                } for doc in docs
            ]
            
            return {
                "answer": answer,
                "sources": sources
            }
        except Exception as e:
            logger.error(f"Manual query failed: {e}")
            return {
                "answer": f"Error processing query: {str(e)}",
                "sources": []
            }

    def get_qa_chain(self, retriever):
        """Mock method for compatibility with main.py stream (Phase 5)."""
        # For simplicity in Phase 5 streaming, we'll implement a minimal wrapper
        class MockChain:
            def __init__(self, service, retriever):
                self.service = service
                self.retriever = retriever
            def invoke(self, inputs):
                res = self.service.query(inputs["query"], self.retriever)
                return {"result": res["answer"]}
        
        return MockChain(self, retriever)

