from rag_query.rag_response import rag

PROMPT = """You are a helpful virtual technology and IT assistant. Use the hotel reviews below as relevant context and sources to help answer the user question. Don't blindly make things up.

SOURCES:
{sources}

QUESTION:
{query}?

ANSWER:"""

if __name__ == "__main__":
    # query = "Best hotel in Istanbul?"
    # response = rag(query=query, prompt=PROMPT)

    # print(response)
    print("---------------------------------------------------------------------------------------------------")
    print("---------------------------------------------------------------------------------------------------")
    print("---------------------------------------------------------------------------------------------------")
    query = "What are some amazing hotels near Big ben?"
    response = rag(query=query, prompt=PROMPT)
    print(response)
