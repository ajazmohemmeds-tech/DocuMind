import logging
from typing import List, Dict, Any, Union
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from app.core.config import settings

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QAChainService:
    """Service for handling QA generation with GPT-4o and source citations."""
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

    def get_qa_chain(self, retriever) -> RetrievalQA:
        """Returns a configured RetrievalQA chain."""
        return RetrievalQA.from_chain_type(
            llm=self.model,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt_template}
        )

    def query(self, question: str, retriever) -> Dict[str, Any]:
        """Runs a query through the QA chain and returns the answer with sources."""
        qa_chain = self.get_qa_chain(retriever)
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
