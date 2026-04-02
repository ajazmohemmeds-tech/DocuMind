import logging
from typing import List, Dict, Any, Union
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from api.core.config import settings

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QAChainService:
    """Service for handling QA generation with GPT-4o and source citations (Simplified)."""
    def __init__(self, model_name: str = settings.OPENAI_MODEL):
        """Initializes the QA chain service."""
        self.model = ChatOpenAI(model=model_name, temperature=0)
        
        # Define a custom prompt to force source citation
        self.prompt_template = PromptTemplate(
            template="""You are a helpful and precise Document Q&A Assistant.
Answer the question below based ONLY on the provided context.
Include source citations (e.g., [Source 1], [Source 2]) in your answer wherever appropriate.
If the context doesn't contain enough information to answer, state that clearly.

Context:
{context}

Question: {question}

Answer with citations:""",
            input_variables=["context", "question"]
        )

    def query(self, question: str, retriever) -> Dict[str, Any]:
        """Runs a manual query by retrieving docs and prompting the LLM."""
        try:
            # 1. Retrieve relevant documents
            docs = retriever.get_relevant_documents(question)
            
            # 2. Format context
            context = "\n\n".join([f"[Source {i+1}]: {doc.page_content}" for i, doc in enumerate(docs)])
            
            # 3. Format prompt
            prompt = self.prompt_template.format(context=context, question=question)
            
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
            logger.error(f"QA query failed: {e}")
            return {"answer": f"Error: {e}", "sources": []}

    def get_qa_chain(self, retriever):
        """Mock for compatibility."""
        class MockChain:
            def __init__(self, service, retriever):
                self.service = service
                self.retriever = retriever
            def invoke(self, inputs):
                res = self.service.query(inputs["query"], self.retriever)
                return {"result": res["answer"]}
        return MockChain(self, retriever)
