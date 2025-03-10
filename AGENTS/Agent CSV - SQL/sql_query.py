import sqlite3


def run_sql_query(db_name, query):
    """
    Executes a SQL query on a SQLite database and returns the results.

    Args:
        db_name (str): The name of the SQLite database file.
        query (str): The SQL query to run.

    Returns:
        list: Query result as a list of tuples, or an empty list if no results or error occurred.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Execute the SQL query
        cursor.execute(query)

        # Fetch all results
        results = cursor.fetchall()

        # Close the connection
        conn.close()

        # Return results or an empty list if no results were found
        return results if results else []

    except sqlite3.Error as e:
        print(f"An error occurred while executing the query: {e}")
        return []


if __name__ == "__main__":
    db_name = "movies_db.db"
    table_name = "movies"

    query = f"SELECT count(*) FROM {table_name};"
    results = run_sql_query(db_name, query)

    if results:
        for row in results:
            print(row)