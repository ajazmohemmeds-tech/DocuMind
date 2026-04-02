import os
import json
import logging
import asyncio
from typing import List, Dict, Any
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from retrieval.retrieval_service import VectorStoreService
from retrieval.qa_service import QAService
from api.core.config import settings

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_evaluation(data_path: str = "./evals/golden_dataset.json"):
    """Runs a RAGAS evaluation (Phase 7)."""
    
    if not os.path.exists(data_path):
        logger.error(f"Golden dataset not found at {data_path}")
        return

    with open(data_path, "r") as f:
        golden_data = json.load(f)

    # Initialize services
    vector_store_service = VectorStoreService()
    qa_service = QAService()
    
    try:
        retriever = vector_store_service.get_retriever()
    except Exception:
        logger.warning("Vector store empty. Evaluating with mock retrieval (if possible) or ensure documents added.")
        return

    # Prepare dataset for RAGAS
    eval_data = {
        "question": [],
        "answer": [],
        "contexts": [],
        "ground_truth": []
    }

    logger.info(f"Running metrics for {len(golden_data)} items...")
    for item in golden_data:
        question = item["question"]
        ground_truth = item["ground_truth"]
        
        # Query our RAG system
        response = qa_service.query(question, retriever)
        
        eval_data["question"].append(question)
        eval_data["answer"].append(response["answer"])
        eval_data["contexts"].append([s["page_content"] for s in response["sources"]])
        eval_data["ground_truth"].append(ground_truth)

    # Convert to datasets.Dataset
    dataset = Dataset.from_dict(eval_data)

    # Run RAGAS metrics
    result = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ],
    )

    logger.info("RAGAS Evaluation Results (Phase 7):")
    logger.info(result)
    
    # Save results to disk
    results_path = "./evals/results.json"
    with open(results_path, "w") as f:
        # Convert result to dict for serialization
        json.dump(result.to_pandas().to_dict(), f, indent=4)
        
    logger.info(f"Results saved to {results_path}")
    return result

if __name__ == "__main__":
    if not settings.OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY is not set.")
    else:
        asyncio.run(run_evaluation())
