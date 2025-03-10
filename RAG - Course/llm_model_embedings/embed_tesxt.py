import ollama  # Assuming ollama Python package is available for local embedding generation
from typing import List
from tenacity import retry, stop_after_attempt, wait_random_exponential
from .model_config  import MODEL_CONFIG


def getembedding(chunks):
    embeds = ollama.embed(model="nomic-embed-text", input=chunks)
    return embeds.get('embeddings', [])


# Embedding model definition from Ollama
# VECTOR_DIMENSIONS = 768  # Adjust according to Ollama model's output
VECTOR_DIMENSIONS = 1024  # Ollama produce a vector size 1024


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
def embed_text(text: List[str], model: str = MODEL_CONFIG["embedding_model"]) -> List[List[float]]:
    """
    Embeds a batch of text strings using the specified model. The model can be
    passed as a parameter, or it will default to the configuration value.

    Parameters:
        text (List[str]): List of text strings to embed.
        model (str): Optional model name to use for embeddings. Defaults to configured model.

    Returns:
        List[List[float]]: List of embeddings for each input text.
    """
    embeddings = []

    for t in text:
        response = ollama.embeddings(prompt=t, model=model)
        embeddings.append(response['embedding'])

        print(f"The embedding dimension is: {len(response['embedding'])}")


    return embeddings
