import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    """Application settings using Pydantic Settings."""
    
    OPENAI_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    MODEL_PROVIDER: str = "openai"  # 'openai', 'google', or 'anthropic'
    
    OPENAI_MODEL: str = "gpt-4o"
    GOOGLE_MODEL: str = "gemini-3.1-pro-preview"
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20240620"
    
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Embedding Configuration: 'openai' or 'local'
    EMBEDDING_TYPE: str = os.environ.get("EMBEDDING_TYPE", "local")
    LOCAL_EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    
    # Data storage settings
    DATA_STORE_PATH: Path = Path("./data")
    FAISS_STORE_PATH: Path = Path("./data/faiss_index")
    
    # RAG settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    CHUNKER_MODE: str = "recursive"  # 'recursive' or 'semantic'
    
    # Service specific configurations
    EN_LANG_BM25: bool = True
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Global Settings Instance
settings = Settings()

# Ensure directories exist
os.makedirs(settings.DATA_STORE_PATH, exist_ok=True)
os.makedirs(settings.FAISS_STORE_PATH, exist_ok=True)
