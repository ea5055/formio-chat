"""Flask application for Form.io integration"""

import json
from flask import Flask, render_template, request, jsonify
from pathlib import Path

app = Flask(__name__, template_folder=Path(__file__).parent / "templates")

# File paths for form schemas
app_dir = Path(__file__).parent
DEFAULT_SCHEMA_FILE = app_dir / "default.json"
FORM_SCHEMA_FILE = app_dir / "form_schema.json"


def load_default_schema():
    """Load the default form schema from default.json"""
    try:
        with open(DEFAULT_SCHEMA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"type": "form", "title": "Form", "display": "form", "components": []}


def load_form_schema():
    """Load the form schema from form_schema.json, or use default if not found"""
    try:
        with open(FORM_SCHEMA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return load_default_schema()


def save_form_schema(schema):
    """Save the form schema to form_schema.json"""
    try:
        with open(FORM_SCHEMA_FILE, 'w') as f:
            json.dump(schema, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving form schema: {e}")
        return False


# Load the form schema on startup
form_schema = load_form_schema()


@app.route("/")
def index():
    """Home page - redirects to editor"""
    return render_template("index.html")


@app.route("/editor")
def editor():
    """Form editor page with form.io editor"""
    return render_template("editor.html", form_schema=json.dumps(form_schema))


@app.route("/form")
def form_page():
    """Form display page where users fill in the form"""
    return render_template("form.html", form_schema=json.dumps(form_schema))


@app.route("/api/form", methods=["GET"])
def get_form():
    """API endpoint to get the current form schema"""
    return jsonify(form_schema)


@app.route("/api/form", methods=["POST"])
def save_form():
    """API endpoint to save the form schema from editor"""
    global form_schema
    
    try:
        # Get the JSON data from the request
        data = request.get_json(force=True, silent=False)
        
        if not data:
            return jsonify({"status": "error", "message": "No form data provided"}), 400
        
        form_schema = data
        
        # Save to file
        if save_form_schema(form_schema):
            return jsonify({"status": "success", "message": "Form saved successfully"})
        else:
            return jsonify({"status": "error", "message": "Failed to save form to file"}), 500
    
    except Exception as e:
        print(f"Error in save_form: {e}")
        return jsonify({"status": "error", "message": f"Error saving form: {str(e)}"}), 400


@app.route("/api/submissions", methods=["POST"])
def submit_form():
    """API endpoint to handle form submissions"""
    data = request.json
    # Here you would typically save the submission to a database
    print(f"Form submission: {data}")
    return jsonify({"status": "success", "message": "Form submitted successfully"})


def main():
    """Main entry point"""
    app.run(debug=True)


if __name__ == "__main__":
    main()
