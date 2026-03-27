from flask import Flask, render_template, jsonify
import wol
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Load config to display the target MAC address in the UI
    try:
        config = wol.load_config()
        mac_address = config.get("mac_address", "Unknown MAC")
    except Exception as e:
        mac_address = "Error loading config"

    return render_template('index.html', mac_address=mac_address)

@app.route('/wake', methods=['POST'])
def wake():
    try:
        # Trigger WOL logic
        result = wol.wake_on_lan()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask development server on all interfaces, listening on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
