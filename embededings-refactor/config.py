import yaml
from pydantic import  Field
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    """
    Configuration class for the RAG system.
    Uses Pydantic for automatic validation and type checking.
    """
    # embed_models: list[str] = Field(..., description="List of embedding models")
    # main_model: str = Field(..., description="Main language model")
    # source_doc_url: str = Field(..., description="URL of the source document")
    # chunk_size: int = Field(..., description="Size of text chunks")
    # questions: list[str] = Field(..., description="List of questions to ask")

    @classmethod
    def from_yaml(cls, path: str = "config/config.yaml"):
        """Load configuration from a YAML file."""
        with open(path, "r") as f:
            return cls(**yaml.safe_load(f))