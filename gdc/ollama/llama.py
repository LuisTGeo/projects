import ollama


def chat_with_ollama(prompt, model="llama3.2"):
    response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
    return response['message']['content'].strip()


def main():
    # Example usage
    prompt = "Tell me a short joke about programming"
    response = chat_with_ollama(prompt)

    if response:
        print("AI Response:", response)


if __name__ == "__main__":
    main()