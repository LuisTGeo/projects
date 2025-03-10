from sqlalchemy import create_engine, text
import pandas as pd
from typing import Generator, Any

# Constants
PROJECT_ID = "postgres"  # Replace with your project ID
DATABASE_URL = f"postgresql://postgres:mysecretpassword@localhost:5432/{PROJECT_ID}"  # Replace with your DB credentials
TABLE_NAME = "hotel_data"
# Initialize database engine


# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Generator to fetch data in batches from PostgreSQL
# Query template for PostgreSQL
QUERY_TEMPLATE = """
SELECT id, review_title, review_text, hotel_name
FROM {table_name}
LIMIT :limit OFFSET :offset;
"""


# Generator to fetch data in batches from PostgreSQL
def query_postgresql_batches(
        max_rows: int,                # Maximum number of rows to fetch from the table
        rows_per_batch: int,          # Number of rows to fetch per batch
        start_batch: int = 0,         # The starting batch (defaults to 0)
        table_mame: str = TABLE_NAME, # Name of the table to query (defaults to a constant)
) -> Generator[pd.DataFrame, Any, None]: # Returns a generator yielding DataFrames
    # Generate batches from a table in PostgreSQL
    with engine.connect() as connection:  # Connect to the PostgreSQL database using SQLAlchemy engine
        for offset in range(start_batch, max_rows, rows_per_batch):  # Loop over data in batches
            # Use SQLAlchemy's `text()` to parameterize the query safely
            query = text(QUERY_TEMPLATE.format(table_name=table_mame))  # Format query with the table name
            result = connection.execute(query, {"limit": rows_per_batch, "offset": offset})  # Execute the query with limits and offsets
            df = pd.DataFrame(result.fetchall(), columns=result.keys())  # Convert the result to a Pandas DataFrame
            # Join title and text fields
            df["content"] = df.apply(lambda r: f"Title: {r.review_title}. Content: {r.review_text}", axis=1)  # Combine "review_title" and "review_text" into one "content" field
            # print("df -----1", df)
            yield df  # Yield the DataFrame as a generator (useful for processing batches without loading everything into memory at once)



# Example usage
if __name__ == "__main__":
    max_rows = 1000  # Total rows to fetch
    rows_per_batch = 100  # Rows per batch

    # Iterate through the batches
    for batch_df in query_postgresql_batches(max_rows, rows_per_batch):
        print(batch_df.head())
