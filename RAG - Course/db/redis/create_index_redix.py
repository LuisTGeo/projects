from redis.commands.search.field import (
    NumericField,
    TagField,
    TextField,
    VectorField,
)
import redis
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query

from llm_model_embedings.model_config import MODEL_CONFIG

# VECTOR_DIMENSIONS = 768  # Ollama produce a vector size 1024
# VECTOR_DIMENSIONS = 1024  # Ollama produce a vector size 1024

INDEX_NAME = "google:idx"
PREFIX = "doc:"
VECTOR_FIELD_NAME = "embedding"

redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Store vectors in redis and create index
def create_redis_index(
        redis_client: redis.Redis,  # Redis client instance
        vector_field_name: str = VECTOR_FIELD_NAME,  # Name of the vector field to be indexed
        index_name: str = INDEX_NAME,  # Name of the Redis index
        prefix: list = [PREFIX],  # List of prefixes for the keys that Redis will search through
        dim: int = MODEL_CONFIG["vector_dimensions"]  # Number of dimensions for the vectors (embeddings)
):
    # Check if an index with the given name already exists
    try:
        redis_client.ft(index_name).info()  # Retrieve information about the index
        print("Existing index found. Dropping and recreating the index", flush=True)
        # If index exists, drop the index but keep the documents
        redis_client.ft(index_name).dropindex(delete_documents=False)
    except:
        # If no index exists, a new one will be created
        print("Creating new index", flush=True)

    # Create the new index
    redis_client.ft(index_name).create_index(
        (
            # Define a vector field with the specified name and indexing parameters
            VectorField(
                vector_field_name, "FLAT",  # Use FLAT indexing method for vector search
                {
                    "TYPE": "FLOAT32",  # Data type of vectors (32-bit float)
                    "DIM": dim,  # Number of dimensions in the vector
                    "DISTANCE_METRIC": "COSINE",  # Distance metric for similarity search (Cosine similarity)
                }
            )
        ),
        # Define index properties such as key prefix and index type
        definition=IndexDefinition(prefix=prefix, index_type=IndexType.HASH)
    )


if __name__ == "__main__":
    # Redis connection (local)
    VECTOR_FIELD_NAME = "embedding"
    create_redis_index(redis_client, vector_field_name=VECTOR_FIELD_NAME)
    print(redis_client.ft(INDEX_NAME).info())

