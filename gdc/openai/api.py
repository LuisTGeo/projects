import os
from openai import OpenAI


def chat_with_gpt(prompt, model="gpt-3.5-turbo"):
    client = OpenAI(api_key="get_key")

    response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
        )

    return response.choices[0].message.content.strip()


def main():
    # Example usage
    prompt = "Tell me a short joke about programming"
    response = chat_with_gpt(prompt)

    if response:
        print("AI Response:", response)


if __name__ == "__main__":
    main()