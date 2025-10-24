# 🚀 Advanced RAG Chatbot Setup Guide

## Overview
This is a comprehensive multi-modal Advanced RAG chatbot with the following features:
- **Multi-modal support** (Text + Images)
- **Multiple LLM providers** (Gemini, Groq, Cohere)
- **Advanced RAG variants** (Basic, Knowledge Graph, Hybrid)
- **Internet search integration**
- **Enhanced guardrails** with toxicity detection
- **Conversation memory** (up to 10 messages)
- **Full observability** with OpenTelemetry

## Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose (for observability stack)
- API keys for your chosen LLM providers

## Quick Start

### 1. Clone and Setup

```bash
git clone <your-repository-url>
cd Advance_RAG_bot
```

### 2. Environment Configuration

Create a `.env` file in the root directory with your API keys:

```env
# LLM API Keys
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
COHERE_API_KEY=your_cohere_api_key_here

# Internet Search
SERPER_API_KEY=your_serper_api_key_here

# Observability (Optional)
OPIK_API_KEY=your_opik_api_key_here
OPIK_ENDPOINT=http://localhost:4318
```

### 3. Backend Setup

```bash
cd backend
pip install -r requirements.txt
python run_server.py
```

### 4. Frontend Setup

```bash
cd frontend
pip install -r requirements.txt
python run_app.py
```

### 5. Access the Application

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## API Keys Setup

### Google Gemini
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add to `.env` as `GEMINI_API_KEY`

### Groq
1. Sign up at [Groq Console](https://console.groq.com/)
2. Generate an API key
3. Add to `.env` as `GROQ_API_KEY`

### Cohere
1. Create account at [Cohere Dashboard](https://dashboard.cohere.ai/)
2. Generate API key
3. Add to `.env` as `COHERE_API_KEY`

### Serper (Internet Search)
1. Sign up at [Serper](https://serper.dev/)
2. Get API key
3. Add to `.env` as `SERPER_API_KEY`

### Opik (Observability)
1. Sign up at [Opik](https://opik.ai/)
2. Get API key
3. Add to `.env` as `OPIK_API_KEY`

## Features

### 🤖 Multi-LLM Support
- **Google Gemini**: Advanced reasoning, multi-modal
- **Groq**: Ultra-fast inference
- **Cohere**: Enterprise-grade models

### 🔍 RAG Variants
- **Basic RAG**: Standard semantic search
- **Knowledge Graph RAG**: Entity relationship reasoning
- **Hybrid RAG**: Combines semantic + internet search

### 🛡️ Enhanced Guardrails
- **Toxicity Detection**: Advanced content filtering
- **NSFW Protection**: Multi-layer content safety
- **Document Relevance**: Context-aware validation

### 🧠 Smart Memory
- **Conversation Context**: Up to 10 previous messages
- **Document Integration**: Context-aware responses
- **Session Management**: Persistent conversation state

### 📊 Observability
- **OpenTelemetry Integration**: Full request tracing
- **Performance Metrics**: Response time monitoring
- **Error Tracking**: Comprehensive logging

## Usage

### 1. Configure Settings
- Select your preferred LLM provider
- Choose RAG variant (Basic/Knowledge Graph/Hybrid)
- Enable/disable internet search

### 2. Upload Documents
- Support for PDF, TXT, DOCX, images
- Multi-document selection
- Real-time processing

### 3. Start Chatting
- Type your questions
- Upload images for multi-modal queries
- Get context-aware responses with sources

### 4. Monitor Performance
- View system status
- Check memory usage
- Monitor conversation history

## Advanced Configuration

### Custom Models
Edit `backend/app/config.py` to add custom models:

```python
CUSTOM_MODELS = {
    "your_provider": ["model1", "model2"]
}
```

### Vector Store
The system uses FAISS for vector storage. Customize in `backend/app/config.py`:

```python
VECTOR_STORE_PATH = "./data/vector_store"
```

### Memory Settings
Adjust conversation memory in `backend/app/services/memory.py`:

```python
MAX_MESSAGES = 10  # Maximum conversation history
```

## Troubleshooting

### Backend Issues
- Check API keys in `.env`
- Verify all dependencies installed
- Check logs for specific errors

### Frontend Issues
- Ensure backend is running on port 8000
- Check browser console for errors
- Verify Streamlit installation

### Performance Issues
- Monitor memory usage
- Check vector store size
- Optimize document processing

## Development

### Adding New LLM Providers
1. Create provider class in `backend/app/services/llm_service.py`
2. Add configuration in `backend/app/config.py`
3. Update frontend options

### Custom RAG Variants
1. Extend `BaseRAG` class in `backend/app/services/rag_service.py`
2. Implement search method
3. Add to RAGFactory

### UI Customization
- Modify CSS in `frontend/app.py`
- Add new components
- Customize styling

## Production Deployment

### Docker Deployment
```bash
docker-compose up -d
```

### Environment Variables
Set production environment variables:
- `DEBUG=false`
- `LOG_LEVEL=INFO`
- Secure API keys

### Monitoring
- Set up Opik dashboard
- Configure alerts
- Monitor performance metrics

## Support

For issues and questions:
1. Check the logs
2. Verify configuration
3. Test with minimal setup
4. Create issue with details

## License

This project is licensed under the MIT License.
