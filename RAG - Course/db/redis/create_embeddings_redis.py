from typing import List
import redis
import numpy as np
import math
from tqdm.auto import tqdm
from db.postgress.query_data_from_postgresql import query_postgresql_batches
from llm_model_embedings.embed_tesxt import embed_text

# Redis connection (local)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Embedding model definition from Ollama
# VECTOR_DIMENSIONS = 768  # Adjust according to Ollama model's output
VECTOR_DIMENSIONS = 1024  # Ollama produce a vector size 1024


# Convert embeddings to bytes for Redis storage
def flat_embedding(emb: List[float]) -> bytes:
    return np.array(emb).astype(np.float32).tobytes()


# Redis key helper function
def redis_key(key_prefix: str, id: str) -> str:
    return f"{key_prefix}:{id}"


# Process a single dataset record
# 3 THREE
def process_record(record: dict) -> dict:
    '''
    Return a new dictionary with selected and processed fields from the original record.
    The fields are filtered to include only the relevant data that will be stored in Redis.
    '''
    return {
        'id': record['id'],  # Unique identifier of the record (assumed to be in the 'id' field)
        'embedding': record['embedding'],  # Embedding data generated for this record (e.g., from text embeddings)
        # embedding containt the info:  df["content"] = df.apply(lambda r: f"Title: {r.review_title}. Content: {r.review_text}", axis=1)  # Combine "review_title" and "review_text" into one "content" field
        'text': record['review_text'],  # Review text content extracted from the original record
        'title': record['review_title']  # Title of the review extracted from the original record
    }


# Load batch of data into Redis as HASH objects
# 2 TWO
def load_redis_batch(
        dataset: list,  # List of records (each record is a dictionary) to be loaded into Redis
        redis_client: redis.Redis = redis_client,  # Redis client instance for interacting with the Redis database
        key_prefix: str = "doc",  # Prefix for Redis keys (default is "doc")
        id_column: str = "id",  # Column name that holds the unique identifier for each record (default is "id")
):
    '''
    Create a Redis pipeline to execute multiple Redis commands in one go for efficiency.
    This reduces the number of round trips between the client and Redis, speeding up the process.
    '''
    pipe = redis_client.pipeline()

    # Iterate through the dataset, processing each record and storing it in Redis
    for i, record in enumerate(tqdm(dataset)):  # Use tqdm to show a progress bar while iterating over the dataset
        # Process each record before loading it into Redis (e.g., remove unwanted fields, normalize data)
        record = process_record(record)

        # Create a Redis key for each record, combining the key prefix (e.g., "doc") with the unique ID
        key = redis_key(key_prefix, record[id_column])  # `redis_key` forms a unique key like "doc:<id>"

        '''
        Use `hset` to store the record in a Redis hash (key-value pairs)
        `mapping=record` means the entire dictionary of the record will be stored as field-value pairs under the hash
        '''
        pipe.hset(key, mapping=record)

    '''
    Execute the pipeline, sending all commands in one go to Redis
    This makes the batch process more efficient by reducing individual calls.
    '''
    pipe.execute()


# Batch embedding generation and Redis loading
# 1 ONE
def create_embeddings_dataset_redis(redis_client, content_query, rows_per_batch):

    '''
    max_rows = 5000  # Define the maximum number of rows to process from the table
    rows_per_batch = 100  # Define the number of rows to process per batch
    Query PostgreSQL data in batches, yielding 100 rows at a time The `query_postgresql_batches` function yields
    one batch of 100 rows at a time instead of loading all 1000 rows at once. If `yield` is replaced with `return`,
    only the first batch (100 rows) would be returned, breaking the batch processing. query_postgresq_batches add a
    new colum that is used to generate the embedding field: df["content"] = df.apply(lambda r: f"Title: {
    r.review_title}. Content: {r.review_text}", axis=1)  # Combine "review_title" and "review_text" into one
    "content" field
    content_query = query_postgresql_batches(max_rows, rows_per_batch, table_mame=table_name)
    '''

    # Iterate over each batch of data from the generator
    for batch in tqdm(content_query):  # Show a progress bar with tqdm
        '''
        Split the batch into smaller chunks for embedding generation.
        Each batch of 100 rows is split into smaller chunks of 5 rows each (100/5 = 20 chunks).
        The use of `np.array_split` ensures that the batch is divided into the desired number of smaller groups.
        '''
        batch_splits = np.array_split(batch, math.ceil(rows_per_batch / 5))
        '''
        Create embeddings for each chunk in the batch
        For each chunk in `batch_splits`, generate embeddings for the "content" field
        Then, convert each generated embedding using the `convert_embedding` function
        '''
        batch["embedding"] = [
            flat_embedding(embedding)  # Convert the raw embedding to a usable format to save it in Redis
            for split in batch_splits  # Loop through each split (sub-batch of 5 rows)
            for embedding in embed_text(split.content)  # Generate embeddings for the "content" column in each split
        ]

        # Convert the batch DataFrame to a list of dictionaries (one per record)
        # This is done to prepare the batch for writing to Redis.
        batch = batch.to_dict("records")

        # Write the processed batch (including the generated embeddings) to Redis
        # `load_redis_batch` is used to insert the batch data into Redis.
        load_redis_batch( batch , redis_client=redis_client)


# Example: Mock dataset and calling the function
if __name__ == "__main__":
    # Mock dataset example
    dataset = [
        {"id": "1", "review_text": "Great hotel with friendly staff.", "review_title": "Excellent stay"},
        {"id": "2", "review_text": "The room was clean but the service was slow.", "review_title": "Decent experience"},
        # Add more records as needed
    ]
    TABLE_NAME = "hotel_data"

    # Process and load embeddings into Redis
    rows_per_batch = 100
    create_embeddings_dataset_redis(redis_client, content_query=dataset, rows_per_batch=rows_per_batch)
