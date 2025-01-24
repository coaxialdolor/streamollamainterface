# Ollama Web Chat Interface

A web-based chat interface for Ollama AI models with real-time streaming capabilities.

## Features

### Frontend
- Modern, clean UI powered by DaisyUI and Tailwind CSS
- Real-time message streaming with typing indicators
- Code syntax highlighting via Prism.js
- LaTeX math rendering with MathJax
- Copy functionality for messages and code blocks
- Fully responsive design for mobile and desktop

### Backend
- Flask server for Ollama communication
- Server-Sent Events (SSE) for streaming
- API Endpoints:
  - `/` - Main chat interface
  - `/chat` - Chat requests and response streaming
  - `/interrupt` - Generation interruption

## Dependencies
```bash
flask>=2.0.0
requests>=2.25.1
python-dotenv>=0.19.0
