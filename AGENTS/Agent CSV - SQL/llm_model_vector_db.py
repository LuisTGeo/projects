import sqlite3
import faiss
import numpy as np
import ollama
from IPython.display import Markdown, display

from prompts import generate_llm_prompt
from sql_query import run_sql_query

VECTOR_DIMENSIONS = 1024  # Ollama produce a vector size 1024

# Initialize the FAISS index
dimension = 768  # 1024  # Dimension size for OpenAI embeddings (may vary by model)
index = faiss.IndexFlatL2(dimension)  # L2 distance index //  # Use IndexFlatL2 with Euclidean distance

# Cache will hold (user_question, sql_query, response)
cache = []


def convert_embedding(emb: list[float]) -> bytes:
    return np.array(emb).astype(np.float32).tobytes()


def get_embeddings(text: str):
    model2 = "nomic-embed-text"  # MODIFY THE DIMENSION 768
    model = "mxbai-embed-large"  # DIMENSION 1024
    response = ollama.embeddings(prompt=text, model=model2)

    print(f"The embedding dimension is: {len(response['embedding'])}")
    return response["embedding"]


def search_cache(question_embedding, threshold=0.1):
    """
    Searches the FAISS index for a similar question.

    Args:
        question_embedding (np.array): The embedding of the user's question.
        threshold (float): The similarity threshold for considering a hit.

    Returns:
        tuple: (sql_query, response) if a hit is found, otherwise None.
    """
    if index.ntotal > 0:
        distances, indices = index.search(np.array([question_embedding]), k=1)
        # print(distances)
        # print(indices)
        # Check if the closest distance is below the threshold
        if distances[0][0] < threshold:
            cache_index = indices[0][0]
            return cache[cache_index][1], cache[cache_index][2]
    return None


def get_table_schema(db_name, table_name):
    """
    Retrieves the schema (columns and data types) for a given table in the SQLite database.

    Args:
        db_name (str): The name of the SQLite database file.
        table_name (str): The name of the table.

    Returns:
        list: A list of tuples with column name, data type, and other info.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Use PRAGMA to get the table schema
    cursor.execute(f"PRAGMA table_info({table_name});")
    schema = cursor.fetchall()

    conn.close()
    return schema


def handle_user_question(user_question: str, table_name: str = "movies", db_name: str = "movies_db.db"):
    """
    Handles the user's question by first searching the cache, and if there's no hit, generating a SQL query and response.

    Args:
        user_question (str): The user's natural language question.

    Returns:
        list: The response to the user's question.
    """
    # Convert the user's question to an embedding
    question_embedding = get_embeddings(user_question)

    # Step 1: Search cache for similar questions -TO IMPROVE -THE QUESTIONS -DATABASE NEED TO HAVE NEEDS ITS OWN INDEX
    cache_hit = search_cache(question_embedding)
    if cache_hit:
        sql_query, response = cache_hit
        print(f"Cache hit! SQL Query: {sql_query}")
        return response

    # Step 2: No hit, go to LLM for SQL generation
    print("Cache miss! Generating SQL from LLM...")

    sql_query = generate_sql_query(question=user_question, table_name=table_name, db_name=db_name)

    # Step 3: Run the SQL query on the database
    response = run_sql_query(db_name, sql_query)

    # Step 4: Store question, SQL, and response in cache
    cache.append((user_question, sql_query, response))
    # index.add(np.array([question_embedding]))  # Add question embedding to FAISS index
    index.add(np.array([question_embedding]))
    print("query ---", sql_query)

    print("response ---", response)
    return response


def generate_sql_query(question: str, table_name: str, db_name: str):
    # table_name = 'movies'
    # db_name = 'movies_db.db'
    table_schema = get_table_schema(db_name, table_name)
    llm_prompt = generate_llm_prompt(table_name, table_schema)
    user_prompt = """Question: {question}"""

    response = ollama.chat(
        model='llama3.2',
        messages=[
            {"content": llm_prompt, "role": "system"},
            {"content": user_prompt.format(question=question), "role": "user"}],
        # {"content": llm_prompt.format(table_name=table_name), "role": "system"},
        # {"content": user_prompt.format(question=question), "role": "user"}],
        stream=False,
    )

    answer = response['message']['content']

    # print("response", response)

    display(Markdown(answer))
    query = answer.replace("```sql", "").replace("```", "")
    query = query.strip()
    return query


if __name__ == '__main__':
    db_name = "movies_db.db"
    table_name = "movies"
    schema = get_table_schema(db_name, table_name)
    print(f"Schema for {table_name}:")
    for col in schema:
        print(col)

    print(" =======  =======  =======  =======  =======  =======  =======  ======= ")
    table_name = "movies"
    schema = get_table_schema(db_name, table_name)
    # Generate the prompt
    llm_prompt = generate_llm_prompt(table_name, schema)
    print(llm_prompt)
