import logging
from typing import List, Dict, Any, Union
# Lazy imports for providers handled in __init__
from typing import List, Dict, Any, Union
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from api.core.config import settings


# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResearchService:
    """Service for generating research insights with Swappable Providers (Phase 4)."""
    def __init__(self):
        """Initializes the research service with support for multiple providers."""
        self.provider = settings.MODEL_PROVIDER.lower()
        self.model = None
        
        try:
            if self.provider == "google":
                if not settings.GOOGLE_API_KEY or "your_" in settings.GOOGLE_API_KEY:
                    logger.warning("GOOGLE_API_KEY is placeholder or missing.")
                else:
                    from langchain_google_genai import ChatGoogleGenerativeAI
                    self.model = ChatGoogleGenerativeAI(
                        model=settings.GOOGLE_MODEL,
                        google_api_key=settings.GOOGLE_API_KEY,
                        temperature=0,
                        streaming=True
                    )
            elif self.provider == "anthropic":
                if not settings.ANTHROPIC_API_KEY or "your_" in settings.ANTHROPIC_API_KEY:
                    logger.warning("ANTHROPIC_API_KEY is placeholder or missing.")
                else:
                    from langchain_anthropic import ChatAnthropic
                    self.model = ChatAnthropic(
                        model=settings.ANTHROPIC_MODEL,
                        anthropic_api_key=settings.ANTHROPIC_API_KEY,
                        temperature=0,
                        streaming=True
                    )
            else: # Default to OpenAI
                if not settings.OPENAI_API_KEY or "your_" in settings.OPENAI_API_KEY:
                    logger.warning("OPENAI_API_KEY is placeholder or missing.")
                else:
                    from langchain_openai import ChatOpenAI
                    self.model = ChatOpenAI(
                        model=settings.OPENAI_MODEL,
                        openai_api_key=settings.OPENAI_API_KEY,
                        temperature=0,
                        streaming=True
                    )
            
            if self.model:
                logger.info(f"Initialized ResearchService with provider: {self.provider}")
        except Exception as e:
            logger.error(f"Failed to initialize {self.provider} model: {e}")
            self.model = None

        
        # Define a custom prompt to force source citation
        self.prompt_template = PromptTemplate(
            template="""You are DocuMind, a precise and scholarly Research Assistant.
Synthesize the information below based ONLY on the provided context.
Include source citations (e.g., [Source 1], [Source 2]) in your response wherever appropriate.
If the context doesn't contain enough information to complete the inquiry, state that clearly.

Context:
{context}

Inquiry: {question}

Response with citations:""",
            input_variables=["context", "question"]
        )

    def get_qa_chain(self, retriever) -> RetrievalQA:
        """Returns a configured RetrievalQA chain (Phase 4)."""
        if not self.model:
            return None
            
        return RetrievalQA.from_chain_type(
            llm=self.model,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt_template}
        )

    def query(self, question: str, retriever) -> Dict[str, Any]:
        """Runs a query through the QA chain and returns the answer with sources."""
        if not self.model:
            return {
                "answer": f"Error: {self.provider.upper()}_API_KEY is not configured correctly. Please update the .env file.",
                "sources": []
            }
            
        qa_chain = self.get_qa_chain(retriever)
        if not qa_chain:
            return {
                "answer": "Error: QA chain could not be initialized.",
                "sources": []
            }
            
        response = qa_chain({"query": question})
        
        # Extract source documents for the citation expander
        source_docs: List[Document] = response.get("source_documents", [])
        sources = [
            {
                "page_content": doc.page_content,
                "metadata": doc.metadata
            } for doc in source_docs
        ]
        
        return {
            "answer": response["result"],
            "sources": sources
        }
