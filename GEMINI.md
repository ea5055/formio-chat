# Form.io Chat Project

## Project Overview
Form.io Chat is a web application designed to integrate Form.io with AI-powered assistance (specifically utilizing Google Gemini). The application allows users to build and fill forms, with an AI assistant that can help with form filling and schema management.

### Key Technologies
- **Backend:** Flask (Python)
- **AI Integration:** Google GenAI (Gemini)
- **Configuration:** python-dotenv for environment management
- **Data Handling:** pandas

## Project Structure
- `src/formio_chat/`: Main source code directory.
  - `app.py`: Flask application routes and logic.
  - `gemini_service.py`: Service wrapper for interacting with the Gemini API.
  - `templates/`: HTML templates for the form editor, display, and chat sidebar.
  - `default.json`, `form_schema.json`: Schema storage files.

## Running the Application
The project is set up as a standard Python project.

### Prerequisites
- Python 3.11+
- `uv` (recommended for dependency management)

### Setup & Execution
1.  Install dependencies:
    ```bash
    uv sync
    ```
2.  Set up environment variables in `.env` (ensure `GEMINI_API_KEY` is set).
3.  Run the application:
    ```bash
    python src/formio_chat/app.py
    # or using the defined script
    formio-chat
    ```

## Development Conventions
- **Codebase Structure:** Follow standard Python project structure with `src/`.
- **Flask:** Adhere to Flask app factory patterns and modular route definitions.
- **AI Service:** Maintain abstraction of the Gemini service in `gemini_service.py` to keep business logic separate from API interactions.
- **Schemas:** Form definitions are stored as JSON files. Always validate schema updates.
