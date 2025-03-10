from flask import Flask, request, jsonify
import os
import re

app = Flask(__name__)

# Define a safe directory for notes.
NOTES_DIR = os.path.join(os.getcwd(), "notes")
if not os.path.exists(NOTES_DIR):
    os.makedirs(NOTES_DIR)

def is_safe_filename(name):
    """
    Only allow filenames with letters, numbers, underscores, and hyphens.
    This prevents directory traversal attempts.
    """
    return re.match(r'^[a-zA-Z0-9_-]+$', name) is not None

@app.route('/put_note', methods=['POST'])
def put_note():
    note = request.json
    if not isinstance(note, dict) or "name" not in note or "value" not in note:
        return jsonify({"ok": False, "error": "invalid note"})
    
    name = note["name"]
    value = note["value"]

    # Validate the filename to prevent injection and directory traversal.
    if not is_safe_filename(name):
        return jsonify({"ok": False, "error": "invalid note name"})
    
    # Build the full file path and ensure it's inside the allowed directory.
    file_path = os.path.join(NOTES_DIR, name)
    if not os.path.abspath(file_path).startswith(os.path.abspath(NOTES_DIR)):
        return jsonify({"ok": False, "error": "invalid file path"})
    
    try:
        with open(file_path, "w") as f:
            f.write(value)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})
    
    return jsonify({"ok": True})

@app.route('/get_note', methods=['POST'])
def get_note():
    note = request.json
    if not isinstance(note, dict) or "name" not in note:
        return jsonify({"ok": False, "error": "invalid note"})
    
    name = note["name"]

    # Validate the filename.
    if not is_safe_filename(name):
        return jsonify({"ok": False, "error": "invalid note name"})
    
    # Build the full file path and ensure it's inside the allowed directory.
    file_path = os.path.join(NOTES_DIR, name)
    if not os.path.abspath(file_path).startswith(os.path.abspath(NOTES_DIR)):
        return jsonify({"ok": False, "error": "invalid file path"})
    
    if not os.path.isfile(file_path):
        return jsonify({"ok": False, "error": "no such note"})
    
    try:
        with open(file_path, "r") as f:
            value = f.read()
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})
    
    return jsonify({"ok": True, "note": value})

if __name__ == "__main__":
    app.run(debug=True)

