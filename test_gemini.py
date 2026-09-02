"""Test script to connect with Gemini LLM model and run a simple query."""

import os
from dotenv import load_dotenv
from google import genai


def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    
    # Create the Generative AI client
    client = genai.Client(api_key=api_key)
    
    # Simple test query
    query = "What is the capital of France?"
    print(f"Query: {query}")
    print("-" * 50)
    
    # Create a chat session and send the query
    chat = client.chats.create(model="gemini-3.5-flash-lite")
    response = chat.send_message(query)
    print(f"Response: {response.text}")
    print("-" * 50)
    print("✓ Successfully connected to Gemini LLM!")


if __name__ == "__main__":
    main()
