# from rag.similarity_search import similarity_search
from query_vector import similarity_search
from llm_model_embedings.question_answer_llm import ollama_response


def create_prompt(prompt_template: str, **kwargs) -> str:
    return prompt_template.format(**kwargs)


def rag(query: str, prompt: str, verbose: bool = True) -> str:
    """
    Simple pipeline for performing retrieval augmented generation with
    Google Vertex PaLM API and Redis Enterprise.
    """
    # Perform a vector similarity search in Redis
    if verbose:
        print("Pulling relevant data sources from Redis", flush=True)
    relevant_sources = similarity_search(query, k=3, return_fields=("text",))
    if verbose:
        print("Relevant sources found!", flush=True)
    # Combine the relevant sources and inject into the prompt
    sources_text = "-" + "\n-".join([source for source in relevant_sources.text.values])
    full_prompt = create_prompt(
        prompt_template=prompt,
        sources=sources_text,
        query=query
    )
    if verbose:
        print("\nFull prompt:\n\n", full_prompt, flush=True)
    # Perform text generation to get a response from PaLM API
    response = ollama_response(prompt=full_prompt)
    return response["response"]


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
