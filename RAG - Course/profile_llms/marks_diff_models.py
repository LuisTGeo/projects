
"""

+REDIS
1. Create the docs in REDIS, for it we need e emmbeded model
2. Create the Index in REDIS, for it we need e emmbeded model

3+ TO SEARCH agains the REDIS database, we need a embebed model to convert the text and run the query agains the VDB
4+

"""
from db.postgress.load_postgres import load_postgresql_from_csv
from db.postgress.query_data_from_postgresql import query_postgresql_batches
from db.redis.create_embeddings_redis import create_embeddings_dataset_redis
import redis

from db.redis.create_index_redix import create_redis_index

redis_client = redis.Redis(host='localhost', port=6379, db=0)


if __name__ == "__main__":
    """
    Load the data into Postgrest
    """
    TABLE_NAME = "hotel_data"
    load_postgresql_from_csv(table_name=TABLE_NAME, csv_path="hotel_datasets_train.csv")

    """It get the data from postgrest' which table=TABLE_NAME, we get the data in Chunks or in a batch process. Each 
    batch data is  passed We define a star_batch, max_rows, rows_per_batch. 
    We get the data in chunks and pass it to a 
    dataframe. Then we create a column "content" that is a string  
    
    form of f"Title: {r.review_title}. Content: {r.review_text}"

    df["content"] = df.apply(lambda r: f"Title: {r.review_title}. Content: {r.review_text}", axis=1)
    yield df
    
    Then we split the df chunk and split it again.  
    """

    max_rows = 5000  # Define the maximum number of rows to process from the table
    rows_per_batch = 100  # Define the number of rows to process per batch

    # Query PostgreSQL data in batches, yielding 100 rows at a time The `query_postgresql_batches` function yields
    # one batch of 100 rows at a time instead of loading all 1000 rows at once. If `yield` is replaced with `return`,
    # only the first batch (100 rows) would be returned, breaking the batch processing. query_postgresq_batches add a
    # new colum that is used to generate the embedding field: df["content"] = df.apply(lambda r: f"Title: {
    # r.review_title}. Content: {r.review_text}", axis=1)  # Combine "review_title" and "review_text" into one
    # "content" field

    content_query = query_postgresql_batches(max_rows, rows_per_batch, table_mame=TABLE_NAME)

    create_embeddings_dataset_redis(redis_client, content_query=content_query, rows_per_batch=rows_per_batch)

    VECTOR_FIELD_NAME = "embedding" # This vector field name is create in create_embeddings_dataset_redis
    create_redis_index(redis_client, vector_field_name=VECTOR_FIELD_NAME)


