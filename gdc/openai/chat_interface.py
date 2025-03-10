import os
import gradio as gr
from openai import OpenAI


def chat_with_gpt(message, history):
    """
    Function to interact with OpenAI's GPT model through Gradio interface

    Args:
        message (str): User's current message
        history (list): Conversation history

    Returns:
        str: AI's response
    """
    client = OpenAI(
        api_key="get_key")

    # Prepare messages including full conversation history
    messages = [
            {"role": "system", "content": "You are a helpful and friendly AI assistant."}
        ]

    # Add previous conversation context
    for human, assistant in history:
            messages.append({"role": "user", "content": human})
            messages.append({"role": "assistant", "content": assistant})

        # Add current user message
    messages.append({"role": "user", "content": message})

        # Generate response
    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300,
            temperature=0.7
        )

    # Extract and return AI's response
    ai_response = response.choices[0].message.content.strip()
    return ai_response


def launch_chat_interface():
    """
    Launch Gradio interface for OpenAI Chat
    """
    # Create Gradio interface
    iface = gr.ChatInterface(
        fn=chat_with_gpt,
        title="OpenAI Chat Interface",
        description="Chat with an AI powered by OpenAI's GPT model",
        theme="soft",
        examples=[
            "Hello, how are you?",
            "Explain quantum computing in simple terms",
            "Write a short poem about technology"
        ],
        cache_examples=False
    )

    # Launch the interface
    iface.launch(
        server_name="0.0.0.0",  # Make accessible on local network
        share=False  # Set to True if you want a public shareable link
    )


# Main execution
if __name__ == "__main__":
    launch_chat_interface()