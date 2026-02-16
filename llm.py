from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Read from environment only (no hard-coded default)
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")

@app.route('/llm', methods=['POST'])
def llm():
    data = request.json
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    if not MISTRAL_API_KEY:
        return jsonify({"error": "MISTRAL_API_KEY not configured"}), 500
    
    try:
        # Use direct HTTP requests instead of mistralai library
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {MISTRAL_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistral-small-latest",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        response.raise_for_status()
        output = response.json()["choices"][0]["message"]["content"]
        return jsonify({"output": output}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=3000, debug=False)
