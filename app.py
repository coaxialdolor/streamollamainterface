from flask import Flask, render_template, request, Response, jsonify
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_stream(prompt):
    payload = {
        "model": "deepseek-r1:14b",
        "prompt": prompt,
        "stream": True
    }
    
    with requests.post(OLLAMA_URL, json=payload, stream=True) as response:
        for chunk in response.iter_lines():
            if chunk:
                data = json.loads(chunk.decode())
                yield f"data: {json.dumps(data)}\n\n"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json['prompt']
    return Response(generate_stream(prompt), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, port=5001)