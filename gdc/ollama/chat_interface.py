import ollama
import gradio as gr

def chat_with_ollama(message, history):
    """
    Function to interact with Ollama's local AI model through Gradio interface

    Args:
        message (str): User's current message
        history (list): Conversation history

    Returns:
        str: AI's response
    """
    try:
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

        # Generate response using Ollama
        response = ollama.chat(
            model="llama3.2",  # You can change this to any model you have downloaded
            messages=messages,
        )

        # Extract and return AI's response
        ai_response = response['message']['content'].strip()
        return ai_response

    except Exception as e:
        return f"An error occurred: {str(e)}"


def launch_chat_interface():
    """
    Launch Gradio interface for Ollama Chat
    """
    # Create Gradio interface
    iface = gr.ChatInterface(
        fn=chat_with_ollama,
        title="Ollama Local AI Chat Interface",
        description="Chat with a local AI model powered by Ollama",
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