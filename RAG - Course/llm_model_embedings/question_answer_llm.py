import ollama

from .model_config import MODEL_CONFIG


# Define the prompt


# Generate response using Ollama's LLaMA model
#  model  llama3.2:3b-instruct-fp16
def ollama_response(prompt: str, model: str = MODEL_CONFIG["prediction_model"]):
    return ollama.generate(model=model, prompt=prompt, stream=False)


if __name__ == "__main__":
    prompt = "What is a large language model?"
    response = ollama_response(prompt=prompt)
    print("response:", response)
    print("Example response:\n", response["response"])
