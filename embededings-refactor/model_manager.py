# model_manager.py
import numpy as np
import ollama
import redis
from redis.commands.search.field import VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from typing import List

class ModelManager:
    """Manages language models, embeddings, and Redis operations."""

    def __init__(self, embed_models: list[str], main_model: str, redis_client: redis.Redis):
        self.embed_models = embed_models
        self.main_model = main_model
        self.redis = redis_client
        self.dim: int = 0

    @staticmethod
    def convert_embedding(emb: List[float]) -> bytes:
        """Convert embedding to bytes for Redis storage."""
        return np.array(emb).astype(np.float32).tobytes()

    def pull_models(self):
        """Pull required models if not available locally."""
        local_models = ollama.list()
        models_to_download = [m for m in self.embed_models + [self.main_model] if m not in local_models]
        for model in models_to_download:
            ollama.pull(model)

    def get_embedding(self, text: list, model_name: str) -> list:
        """Get embeddings for given text using specified model."""
        embedding = ollama.embed(model=model_name, input=text)
        self.dim = len(embedding['embeddings'][0]) # text, it is a list of text str
        return embedding['embeddings']

    def create_redis_index(self, model_name: str, vector_field_name: str = "embedding"):
        """Create or recreate Redis index for vector search."""
        try:
            self.redis.ft(f"idx:{model_name}").dropindex(delete_documents=False)
        except:
            pass

        self.redis.ft(f"idx:{model_name}").create_index(
            (VectorField(vector_field_name, "FLAT", {"TYPE": "FLOAT32", "DIM": self.dim, "DISTANCE_METRIC": "COSINE"}),),
            definition=IndexDefinition(prefix=[f"{model_name}:"], index_type=IndexType.HASH)
        )

    def add_items(self, text_chunks: list, model_name: str):
        """Add text chunks and their embeddings to Redis."""
        embeddings = self.get_embedding(text_chunks, model_name)
        for i, (chunk, embedding) in enumerate(zip(text_chunks, embeddings)):
            doc_id = f"{model_name}:{i}"
            self.redis.hset(doc_id, mapping={"embedding": self.convert_embedding(embedding), "text": chunk})

    def similarity_search(self, query_embedding: list, model_name: str, k: int, return_fields: tuple):
        """Perform similarity search in Redis."""
        index_name = f"idx:{model_name}"
        redis_query = (
            Query(f"*=>[KNN {k} @embedding $embedding AS score]")
            .sort_by("score")
            .return_fields(*return_fields)
            .paging(0, k)
            .dialect(2)
        )
        results = self.redis.ft(index_name).search(
            redis_query, query_params={"embedding": self.convert_embedding(query_embedding[0])}
        )
        return results

    def ask_question(self, question: str, context: str = "") -> str:
        """Generate answer for a question using the main model."""
        prompt = f"{question}\nContext: {context}" if context else question
        response = ollama.generate(model=self.main_model, prompt=prompt)
        return response['response']