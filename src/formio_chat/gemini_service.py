"""Gemini LLM service for form assistance."""

import json
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

class GeminiFormAssistant:
    """AI assistant for helping users fill forms using Gemini LLM."""
    
    def __init__(self):
        """Initialize the Gemini assistant."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables. "
                "Please create a .env file with GEMINI_API_KEY set. "
                "See .env.example for reference."
            )
        
        try:
            self.client = genai.Client(api_key=api_key)
        except Exception as e:
            raise ValueError(
                f"Failed to initialize Gemini API: {str(e)}. "
                "Check that your API key is valid."
            )
    
    def get_assistant_prompt(self, form_schema: dict, current_data: dict, user_message: str) -> str:
        """Generate a system prompt for the Gemini assistant."""
        form_components = []
        for component in form_schema.get("components", []):
            if component.get("type") != "button":
                field_info = {
                    "key": component.get("key"),
                    "label": component.get("label"),
                    "type": component.get("type"),
                    "placeholder": component.get("placeholder", ""),
                    "required": component.get("required", False),
                }
                form_components.append(field_info)
        
        prompt = f"""You are a helpful form assistant. You help users fill out forms by updating form fields based on their natural language requests.

Current Form Schema:
{json.dumps(form_components, indent=2)}

Current Form Data:
{json.dumps(current_data, indent=2)}

User Request: {user_message}

Your task:
1. Understand what the user wants to do with the form
2. Identify which form fields need to be updated
3. Provide both:
   a) A friendly response to the user explaining what you'll do
   b) A JSON object with the field updates in this exact format:
   
   FIELD_UPDATES: {{"fieldKey": "value", "anotherField": "value"}}
   
4. If the user asks a question about the form structure, answer it naturally
5. If you can't update something, explain why in your response

IMPORTANT: Always include the FIELD_UPDATES line with a JSON object, even if it's empty: FIELD_UPDATES: {{}}

Keep your response conversational and helpful."""
        
        return prompt
    
    def process_user_request(self, form_schema: dict, current_data: dict, user_message: str) -> dict:
        """
        Process a user request and return both AI response and field updates.
        
        Returns:
            dict: {
                "message": "AI's response to the user",
                "updates": {"fieldKey": "value", ...},
                "error": None or error message
            }
        """
        try:
            prompt = self.get_assistant_prompt(form_schema, current_data, user_message)
            
            # Use Chat API to avoid deprecation warning about AFC
            chat = self.client.chats.create(model="gemini-3.5-flash-lite")
            response = chat.send_message(prompt)
            response_text = response.text
            
            # Extract field updates from the response
            updates = {}
            if "FIELD_UPDATES:" in response_text:
                try:
                    # Find the JSON part after FIELD_UPDATES:
                    start_idx = response_text.index("FIELD_UPDATES:") + len("FIELD_UPDATES:")
                    json_str = response_text[start_idx:].strip()
                    
                    # Find the JSON object
                    brace_start = json_str.index("{")
                    brace_count = 0
                    brace_end = brace_start
                    
                    for i in range(brace_start, len(json_str)):
                        if json_str[i] == "{":
                            brace_count += 1
                        elif json_str[i] == "}":
                            brace_count -= 1
                            if brace_count == 0:
                                brace_end = i + 1
                                break
                    
                    json_part = json_str[brace_start:brace_end]
                    updates = json.loads(json_part)
                except (ValueError, IndexError, json.JSONDecodeError) as e:
                    # If we can't parse updates, that's okay - just extract the message
                    pass
            
            # Remove the FIELD_UPDATES line from the message
            message = response_text.split("FIELD_UPDATES:")[0].strip()
            
            return {
                "message": message,
                "updates": updates,
                "error": None
            }
        
        except Exception as e:
            return {
                "message": "Sorry, I encountered an error processing your request.",
                "updates": {},
                "error": str(e)
            }


def get_gemini_assistant():
    """Factory function to get or create the Gemini assistant."""
    if not hasattr(get_gemini_assistant, "_instance"):
        get_gemini_assistant._instance = GeminiFormAssistant()
    return get_gemini_assistant._instance
