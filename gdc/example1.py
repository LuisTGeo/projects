import ollama
import uuid
import json
import os
from typing import List, Dict, Optional


class OllamaChatInterface:
    def __init__(self,
                 model: str = 'llama3',
                 history_file: Optional[str] = None,
                 max_history_length: int = 10):
        """
        Initialize the Ollama Chat Interface

        Args:
            model (str): Ollama model to use for chat
            history_file (str, optional): Path to save/load conversation history
            max_history_length (int): Maximum number of previous messages to retain
        """
        self.model = model
        self.history_file = history_file or f'chat_history_{uuid.uuid4()}.json'
        self.max_history_length = max_history_length
        self.conversation_history: List[Dict] = []

        # Load existing history if file exists
        self.load_history()

    def load_history(self):
        """Load conversation history from file if it exists"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    self.conversation_history = json.load(f)
            except Exception as e:
                print(f"Error loading history: {e}")
                self.conversation_history = []

    def save_history(self):
        """Save conversation history to file"""
        # Trim history if it exceeds max length
        if len(self.conversation_history) > self.max_history_length:
            self.conversation_history = self.conversation_history[-self.max_history_length:]

        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.conversation_history, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")

    def generate_response(self, user_message: str) -> str:
        """
        Generate a response using Ollama

        Args:
            user_message (str): User's input message

        Returns:
            str: Generated response from the model
        """
        # Prepare messages with conversation history
        messages = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in self.conversation_history
        ]
        messages.append({"role": "user", "content": user_message})

        try:
            # Generate response from Ollama
            response = ollama.chat(
                model=self.model,
                messages=messages
            )

            # Extract and store the response
            ai_response = response['message']['content']

            # Update conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_response
            })

            # Save updated history
            self.save_history()

            return ai_response

        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm sorry, but I encountered an error processing your message."

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
        print("Conversation history has been cleared.")

    def interactive_chat(self):
        """
        Start an interactive chat session
        Allows continuous conversation with the option to exit
        """
        print(f"Starting chat with {self.model} model. Type 'exit' to end the conversation.")
        print("Type 'clear' to reset conversation history.")

        while True:
            try:
                user_input = input("You: ").strip()

                if user_input.lower() == 'exit':
                    break

                if user_input.lower() == 'clear':
                    self.clear_history()
                    continue

                if user_input:
                    response = self.generate_response(user_input)
                    print(f"AI: {response}\n")

            except KeyboardInterrupt:
                print("\nChat interrupted. Exiting...")
                break

        print("Chat session ended.")


def main():
    """Main function to demonstrate chat interface"""
    # You can specify different models or customize parameters
    chat_interface = OllamaChatInterface(
        model='llama3.2',  # Change this to your preferred Ollama model
        max_history_length=10
    )

    chat_interface.interactive_chat()


if __name__ == '__main__':
    main()

# Installation Requirements:
# 1. Install Ollama from https://ollama.com/
# 2. Pull your desired model: ollama pull llama3
# 3. pip install ollama
#
# Usage Tips:
# - This script maintains conversation context
# - Supports clearing history
# - Saves conversation to a unique JSON file
# - Trims history to prevent excessive memory usage