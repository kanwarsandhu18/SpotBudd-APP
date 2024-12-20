from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pytesseract
from PIL import Image
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Folder to save uploaded images
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def home():
    return "Flask server is running!"

# Endpoint to upload a file
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected for uploading"}), 400
    print("file")
    if file:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)  # Save the file
        extracted_text = extract_text_from_image(filepath)
        os.remove(filepath)
        return {"text": extracted_text}, 200

    return jsonify({"error": "File upload failed"}), 500

def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # Runs on localhost:5000
