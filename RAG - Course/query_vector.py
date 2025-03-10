import pandas as pd
from pandas import DataFrame
from redis.commands.search.query import Query
from db.redis.create_embeddings_redis import embed_text, flat_embedding
from clients import redis_client

query = "What is the best hotel close to the Louvre?"
query_vector = embed_text([query])[0]

# Our query has been converted to a list of floats (this is a truncated view)
var = query_vector[:10]
print(var)

redis_client = redis_client()
INDEX_NAME = "google:idx"
VECTOR_FIELD_NAME = "embedding"


# Helper method to perform KNN similarity search in Redis
def similarity_search(query: str, k: int, return_fields: tuple, index_name: str = INDEX_NAME) -> DataFrame:
    # create embedding from query text
    query_vector = embed_text([query])[0]
    # create redis query object
    redis_query = (
        Query(f"*=>[KNN {k} @{VECTOR_FIELD_NAME} $embedding AS score]")
        .sort_by("score")
        .return_fields(*return_fields)
        .paging(0, k)
        .dialect(2)
    )
    # execute the search
    results = redis_client.ft(index_name).search(
        redis_query, query_params={"embedding": flat_embedding(query_vector)}
    )
    return pd.DataFrame([t.__dict__ for t in results.docs]).drop(columns=["payload"])



if __name__ == "__main__":
    # 2. Perform vector similarity search with given query
    results = similarity_search(query, k=5, return_fields=("score", "title", "text", "id"))
    print("id --", results["id"])
    print("score ---", results["score"])
    print("title --", results["title"])
    # print(results)