# AI Form Assistant Feature

This feature adds an AI-powered chat assistant to the "Fill Form" page, allowing users to interact naturally with an AI to populate form fields.

## Overview

The AI Form Assistant is built using:
- **Backend**: Flask API endpoint (`/api/chat`) with Gemini LLM integration
- **Frontend**: JavaScript chat UI with browser-based chat history
- **Service**: `gemini_service.py` - Handles all Gemini API interactions

## Architecture

```
/src/formio_chat/
├── gemini_service.py           # Gemini LLM service (separate module)
├── app.py                       # Updated with /api/chat endpoint
└── templates/
    ├── form.html                # Updated to include chat sidebar
    ├── ai_chat_sidebar.html     # Chat UI component (separate file)
    └── ...
```

## Features

### 1. **Natural Language Form Filling**
Users can request form updates in natural language:
- "Set my name to John Doe"
- "Fill all the fields with sample data"
- "What fields are required?"

### 2. **AI-Powered Updates**
The Gemini API:
- Understands the form schema structure
- Knows current form values
- Generates appropriate field updates
- Validates field types before suggesting changes

### 3. **Change Confirmation Workflow**
- AI shows proposed changes
- User must confirm before applying
- Changes appear in real-time in the form

### 4. **Persistent Chat History**
- Conversation history saved in browser localStorage
- Survives page reloads
- Can be cleared by calling `window.formAssistant.clearHistory()`

### 5. **Multiple AI Capabilities**
- Fill specific fields
- Generate realistic test data
- Answer questions about form structure
- Suggest corrections for form data
- Validate data against field types

## Setup

### 1. Install Dependencies
```bash
pip install google-generativeai python-dotenv
# Or use uv
uv sync
```

### 2. Configure Gemini API

Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your API key from: https://ai.google.dev/

### 3. Run the Application
```bash
python -m formio_chat.app
# Or
formio-chat
```

## File Structure

### New Files Created:
- `gemini_service.py` - Gemini LLM integration (reusable service)
- `ai_chat_sidebar.html` - Chat UI template (includes CSS and JavaScript)

### Modified Files:
- `app.py` - Added `/api/chat` endpoint and Gemini imports
- `form.html` - Included AI chat sidebar
- `pyproject.toml` - Added dependencies

## API Endpoint

### POST `/api/chat`

**Request:**
```json
{
  "message": "User's natural language request",
  "formData": {
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "message": "AI's response to the user",
  "updates": {
    "fieldKey": "updated value",
    "anotherField": "another value"
  },
  "error": null
}
```

## How It Works

### User Interaction Flow:
1. User types a message in the chat input
2. Message is sent to `/api/chat` with current form data
3. Gemini processes the request and returns:
   - A friendly response message
   - Proposed field updates
4. Chat shows proposed changes for user confirmation
5. User clicks "Apply" or "Cancel"
6. If approved, fields are updated in the form

### Gemini Prompt Engineering:
The system prompt tells Gemini:
- The complete form schema (fields, types, requirements)
- Current form data
- User's natural language request
- Expected output format (JSON field updates)
- Format for responses (message + FIELD_UPDATES JSON)

## Customization

### Styling
Edit the CSS in `ai_chat_sidebar.html` to customize colors, layout, and appearance.

### Capabilities
To add or remove capabilities, modify the system prompt in `gemini_service.py` method `get_assistant_prompt()`.

### AI Behavior
Adjust Gemini model or parameters in `gemini_service.py`:
- Change model: `self.model = genai.GenerativeModel("model-name")`
- Adjust temperature, top_p, etc. in `model.generate_content()` call

## Troubleshooting

### Chat feature unavailable
- Check `.env` file contains `GEMINI_API_KEY`
- Check API key is valid
- Look at server logs for errors

### Changes not applying
- Open browser console (F12) to see JavaScript errors
- Verify form field names match the ones Gemini suggests
- Check that form fields have `name` attribute

### Chat history not persisting
- Browser localStorage might be disabled
- Check browser privacy settings
- History is cleared automatically on incognito mode

## Future Enhancements

Possible improvements:
- Image input support (user uploads form image)
- Multi-language support
- Form field validation hints
- Integration with form submission tracking
- Admin dashboard for monitoring AI usage
- Custom system prompts per form
- Cost optimization with token counting

## Code Quality

The code is organized to keep AI functionality separate:
- `gemini_service.py` can be used independently
- `ai_chat_sidebar.html` is a self-contained component
- Easy to test, modify, or extend

## License

Same as the main project.
