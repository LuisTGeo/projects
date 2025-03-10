def generate_llm_prompt(table_name, table_schema):
    """
    Generates a prompt to provide context about a table's schema for LLM to convert natural language to SQL.

    Args:
        table_name (str): The name of the table.
        table_schema (list): A list of tuples where each tuple contains information about the columns in the table.

    Returns:
        str: The generated prompt to be used by the LLM.
    """
    prompt = f"""You are an expert in writing SQL queries for relational databases. 
    You will be provided with a database schema and a natural 
    language question, and your task is to generate an accurate SQL query.

    The database has a table named '{table_name}' with the following schema:\n\n"""

    prompt += "Columns:\n"

    for col in table_schema:
        column_name = col[1]
        column_type = col[2]
        prompt += f"- {column_name} ({column_type})\n"

    prompt += "\nPlease generate a SQL query based on the following natural language question. ONLY return the SQL query."


    return prompt