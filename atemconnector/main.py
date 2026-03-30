from src.config_manager import ConfigManager
from src.ATEM import PyAtemMax
from src.LabelController import LabelController

from flask import Flask, jsonify, request

app = Flask(__name__)

config = ConfigManager()
[host, port] = config.get_connection_information()
atem = PyAtemMax(host, port)
labels = LabelController(atem, config)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"})

@app.route("/labels", methods=["GET"])
def get_labels():
    return jsonify(labels.get_all_labels())

@app.route("/labels/<label_id>", methods=["POST"])
def update_label(label_id):
    data = request.json
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400
    
    new_text = data["text"]
    try:
        labels.assign_camera_operator(label_id, new_text)
        return jsonify({"status": "success", "label_id": label_id, "new_text": new_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    if not atem.connect():
        raise Exception("Failed to connect to ATEM switcher. Please check connection settings.")
    app.run(host="127.0.0.1", port=8765)