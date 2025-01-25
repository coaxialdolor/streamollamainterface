from flask import Flask, render_template, request, Response, jsonify
import requests
import json
import os
import sys
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
OLLAMA_URL = "http://localhost:11434/api/generate"
is_streaming = False  # Global variable to track streaming state

def generate_stream(prompt):
    global is_streaming
    is_streaming = True
    payload = {
        "model": "deepseek-r1:14b",
        "prompt": prompt,
        "stream": True
    }
    
    try:
        with requests.post(OLLAMA_URL, json=payload, stream=True) as response:
            for chunk in response.iter_lines():
                if chunk and is_streaming:
                    data = json.loads(chunk.decode())
                    yield f"data: {json.dumps(data)}\n\n"
                else:
                    break
    finally:
        is_streaming = False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json['prompt']
    return Response(generate_stream(prompt), mimetype='text/event-stream')

@app.route('/interrupt', methods=['POST'])
def interrupt():
    global is_streaming
    is_streaming = False
    return jsonify({"status": "interrupted"})

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func:
        shutdown_func()
    return jsonify({"status": "shutdown"})

@app.route('/restart', methods=['POST'])
def restart():
    def restart_server():
        python = sys.executable
        os.execl(python, python, *sys.argv)
    
    try:
        restart_server()
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
    return jsonify({"status": "restarting"})

if __name__ == '__main__':
    app.run(debug=True, port=5001)