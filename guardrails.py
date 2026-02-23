# Generated with GitHub Copilot (Claude Opus)
from flask import Flask, request, jsonify
import re
import requests
import os

app = Flask(__name__)

# Read from environment variable (strip trailing slash to avoid double slashes)
FIREBASE_DB = os.environ.get('FIREBASE_DB', '').rstrip('/')

@app.route('/guardrails/<id>', methods=['PUT'])
def create_guardrail(id):
    data = request.json
    
    # Validate ID mismatch if body contains id
    body_id = data.get("id")
    if body_id is not None and body_id != id:
        return jsonify({"error": "ID mismatch"}), 400
    
    regx = data.get('regx')
    sub = data.get('sub')
    
    if not regx or sub is None:
        return jsonify({"error": "Missing regx or sub"}), 400
    
    # Validate regex
    try:
        re.compile(regx)
    except re.error:
        return jsonify({"error": "Invalid regex"}), 400
    
    # Store in Firebase
    guardrail = {"id": id, "regx": regx, "sub": sub}
    response = requests.put(f'{FIREBASE_DB}/guardrails/{id}.json', json=guardrail)
    
    if response.status_code == 200:
        return jsonify(guardrail), 201
    return jsonify({"error": "Failed to store"}), 500

@app.route('/guardrails/<id>', methods=['GET'])
def get_guardrail(id):
    response = requests.get(f'{FIREBASE_DB}/guardrails/{id}.json')
    if response.status_code == 200 and response.json():
        return jsonify(response.json()), 200
    return jsonify({"error": "Not found"}), 404

@app.route('/guardrails', methods=['GET'])
def get_all_guardrails():
    response = requests.get(f'{FIREBASE_DB}/guardrails.json')
    if response.status_code == 200:
        data = response.json() or {}
        ids = list(data.keys())
        return jsonify(ids), 200
    return jsonify([]), 200

@app.route('/guardrails/<id>', methods=['DELETE'])
def delete_guardrail(id):
    # First check if resource exists
    check = requests.get(f'{FIREBASE_DB}/guardrails/{id}.json')
    if check.status_code != 200 or check.json() is None:
        return jsonify({"error": "Not found"}), 404
    
    response = requests.delete(f'{FIREBASE_DB}/guardrails/{id}.json')
    if response.status_code == 200:
        return "", 204
    return jsonify({"error": "Delete failed"}), 500

if __name__ == '__main__':
    app.run(port=3001, debug=False)