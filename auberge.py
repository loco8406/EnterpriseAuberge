# Generated with GitHub Copilot (Claude Opus)
from flask import Flask, request, jsonify
import requests
import re
import os

app = Flask(__name__)

LLM_URL = os.environ.get("LLM_URL", "http://localhost:3000/llm")
GUARDRAILS_URL = os.environ.get("GUARDRAILS_URL", "http://localhost:3001/guardrails")

def fetch_guardrails():
    """Fetch list of guardrail IDs, then retrieve each guardrail."""
    rsp = requests.get(GUARDRAILS_URL)
    if rsp.status_code != 200:
        return []
    ids = rsp.json() or []
    guardrails = []
    for gid in ids:
        gr_rsp = requests.get(f"{GUARDRAILS_URL}/{gid}")
        if gr_rsp.status_code == 200:
            guardrail = gr_rsp.json()
            if "regx" in guardrail and "sub" in guardrail:
                guardrails.append(guardrail)
    return guardrails

@app.route('/auberge', methods=['POST'])
def auberge():
    data = request.json or {}
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    try:
        guardrails = fetch_guardrails()
    except Exception as e:
        guardrails = []
    
    # Apply guardrails to input prompt
    sanitised_prompt = prompt
    for g in guardrails:
        regx = g.get('regx')
        sub = g.get('sub')
        if regx and sub is not None:
            try:
                sanitised_prompt = re.sub(regx, sub, sanitised_prompt)
            except re.error:
                continue
    
    # Call LLM with sanitised prompt
    try:
        llm_rsp = requests.post(LLM_URL, json={"prompt": sanitised_prompt})
    except Exception as e:
        return jsonify({"error": f"LLM service error: {str(e)}"}), 500
    
    if llm_rsp.status_code != 200:
        return jsonify({"error": "LLM service failed"}), 500
    
    llm_json = llm_rsp.json() or {}
    output = llm_json.get('output')
    if output is None:
        return jsonify({"error": "LLM response missing output"}), 500
    
    # Apply guardrails to output
    sanitised_output = output
    for g in guardrails:
        regx = g.get('regx')
        sub = g.get('sub')
        if regx and sub is not None:
            try:
                sanitised_output = re.sub(regx, sub, sanitised_output)
            except re.error:
                continue
    
    return jsonify({"output": sanitised_output}), 200

if __name__ == '__main__':
    app.run(port=3002, debug=False)