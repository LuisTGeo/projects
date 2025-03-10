from llm_model_vector_db import handle_user_question

# if __name__ == '__main__':
    # # question = "total number of movies are made by Warner Bros company in year 2008?"
    # # question = "how many movies have RottenTomatoes scores lower than 85?"
    #
    # db_name = "emissions_metrics_db.db"
    # table_name = "emissions_metrics"
    #
    # question = "how many buildings have roof height equal to 5"
    # handle_user_question(user_question=question, table_name=table_name,
    #                      db_name=db_name)
    #
    # print(" ----- ")
    # print(" ----- ")
    # question_2 = "how many buildings have roof height greater than 5"
    # handle_user_question(user_question=question_2, table_name=table_name,
    #                      db_name=db_name)
    #
    # print(" ----- ")
    # print(" ----- ")
    # question_3 = "how many buildings have roof height lower than 5?"
    # handle_user_question(user_question=question_3, table_name=table_name,
    #                      db_name=db_name)
    # print(" ----- ")
    # print(" ----- ")
    # # question = "how many movies with action genre are in the database"
    # # handle_user_question(user_question=question)






import asyncio
import argparse
import shutil
import logging
import ollama
from llm_model_vector_db import get_embeddings, search_cache, run_sql_query, get_table_schema, generate_llm_prompt
import numpy as np

# Assuming you have a cache and index defined somewhere
cache = []
index = None  # This should be properly initialized with your FAISS index

async def speak(speaker, content):
    if speaker and content.strip():
        try:
            p = await asyncio.create_subprocess_exec(speaker, content)
            await p.communicate()
        except Exception as e:
            logging.error(f"Failed to speak content: {e}")

async def generate_sql_query(question: str, table_name: str, db_name: str, client):
    table_schema = get_table_schema(db_name, table_name)
    llm_prompt = generate_llm_prompt(table_name, table_schema)
    user_prompt = f"Question: {question}"

    response = await client.chat(
        model='llama3.2',
        messages=[
            {"content": llm_prompt, "role": "system"},
            {"content": user_prompt, "role": "user"}
        ],
        stream=False
    )

    answer = response['message']['content']
    query = answer.replace("```sql", "").replace("```", "").strip()
    return query

async def handle_user_question2(user_question: str, table_name: str, db_name: str, client):
    question_embedding = get_embeddings(user_question)

    cache_hit = search_cache(question_embedding)
    if cache_hit:
        sql_query, response = cache_hit
        print(f"Cache hit! SQL Query: {sql_query}")
        return response

    print("Cache miss! Generating SQL from LLM...")

    sql_query = await generate_sql_query(question=user_question, table_name=table_name, db_name=db_name, client=client)

    response = run_sql_query(db_name, sql_query)

    # cache.append((user_question, sql_query, response))
    # index.add(np.array([question_embedding]))

    print("Query:", sql_query)
    print("Response:", response)
    return response

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--speak', default=False, action='store_true')
    parser.add_argument('--db_name', default='emissions_metrics_db.db')
    parser.add_argument('--table_name', default='emissions_metrics')
    args = parser.parse_args()

    speaker = None
    if args.speak:
        speaker = shutil.which('say') or shutil.which('espeak') or shutil.which('espeak-ng')

    client = ollama.AsyncClient()

    while True:
        content_in = input('>>> ')
        if not content_in:
            continue

        response = await handle_user_question2(content_in, args.table_name, args.db_name, client)

        content_out = ''
        for char in str(response):
            print(char, end='', flush=True)
            content_out += char
            if char in ['.', '!', '?', '\n']:
                await speak(speaker, content_out)
                content_out = ''

        if content_out:
            await speak(speaker, content_out)
        print()

if __name__ == '__main__':
    asyncio.run(main())