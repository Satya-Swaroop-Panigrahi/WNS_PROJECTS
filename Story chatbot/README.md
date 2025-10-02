# 🤖 Story Chatbot - AI Content Generator

A comprehensive AI-powered chatbot built with Streamlit that generates stories, jokes, and responses using multiple Large Language Models (LLMs). Features include web search capabilities, image generation, text-to-speech, and robust content filtering with guardrails.

## ✨ Features

### Core Functionality
- **Multi-LLM Support**: Integrates with Groq (Llama), OpenAI (GPT), and Google (Gemini)
- **Content Types**: Generate stories, jokes, and chat responses
- **Genre Selection**: Choose from Adventure, Fantasy, Mystery, Romance, Sci-Fi, Horror, Comedy, Drama, Thriller, and Children's content
- **Age-Appropriate Content**: Tailor content for different age groups (Children 5-12, Teen 13-17, Young Adult 18-25, Adult 26-50, Senior 50+)

### Advanced Features
- **Web Search Integration**: Safe web search with content filtering
- **Image Generation**: Create images based on generated stories using DALL-E
- **Text-to-Speech**: Convert generated content to audio
- **Content Filtering**: Built-in guardrails to prevent sensitive or biased content
- **Model Selection**: Dropdown to choose between different LLM versions
- **Parameter Control**: Sliders for temperature and token count adjustment

### Safety & Guardrails
- **Content Filtering**: Prevents generation of harmful, offensive, or inappropriate content
- **Bias Prevention**: Avoids content that discriminates against religion, race, language, or country
- **Safe Search**: Web search queries are filtered for safety
- **Error Handling**: Graceful fallbacks when models are unavailable

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- API Keys for (Free Tier):
  - OpenAI (for GPT models and DALL-E) - $5 free credit
  - Groq (for Llama models) - 30 requests/minute
  - Google (for Gemini models) - 15 requests/minute
  - SerpAPI (for web search) - 100 free searches/month

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd story-chatbot
   ```

2. **Install Dependencies**
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   SERPAPI_KEY=your_serpapi_key_here
   ```

### Running the Application

**Option 1: Using the Runner Script (Recommended)**
```bash
python run.py
```

**Option 2: Direct Streamlit Command**
```bash
streamlit run streamlit_app.py
```

The application will open in your default browser at `http://localhost:8501`

## 🏗️ Architecture

### Project Structure
```
├── streamlit_app.py      # Main Streamlit application
├── config.py            # Configuration and settings
├── run.py               # Application runner script
├── requirements.txt     # Python dependencies
├── services/           # Service modules
│   ├── __init__.py
│   ├── llm_service.py  # LLM integration (Groq, OpenAI, Gemini)
│   ├── content_filter.py # Content safety and filtering
│   ├── web_search_service.py # Web search functionality
│   ├── image_service.py # Image generation (DALL-E)
│   └── tts_service.py  # Text-to-speech functionality
└── README.md           # This file
```

### Streamlit App Features
- **Interactive UI**: Clean, responsive interface with sidebar controls
- **Real-time Generation**: Instant content generation with loading indicators
- **Multiple Actions**: Generate, search, create images, and text-to-speech
- **Session State**: Maintains content across interactions
- **Error Handling**: User-friendly error messages and fallbacks

## 🎛️ Configuration Options

### Supported Models (Free Tier Only)
- **Groq**: llama-3.1-8b-instant (30 req/min), gemma2-9b-it (30 req/min)
- **OpenAI**: gpt-3.5-turbo ($5 free credit for new users)
- **Gemini**: gemini-2.5-flash (15 req/min), gemini-2.5-pro (15 req/min), gemini-2.0-flash (experimental)

### Content Types
- **Story**: Creative narratives with characters, plot, and setting
- **Joke**: Clean, funny jokes and puns
- **Chat**: Conversational responses and Q&A

### Parameters
- **Temperature**: 0.0 - 2.0 (controls creativity/randomness)
- **Max Tokens**: 100 - 2000 (controls response length)

## 🛡️ Safety Features

### Content Filtering
The application includes multiple layers of content filtering:

1. **Sensitive Content Detection**: Filters violence, explicit content, hate speech
2. **Bias Prevention**: Prevents discriminatory content based on religion, race, etc.
3. **Search Safety**: Validates web search queries for appropriateness
4. **Image Safety**: Validates image generation prompts

### Error Handling
- Graceful fallbacks when APIs are unavailable
- Clear error messages for users
- Automatic retry mechanisms for transient failures

## 🎨 User Interface

### Streamlit Design Features
- **Modern Interface**: Clean, professional design with custom CSS styling
- **Responsive Layout**: Works on desktop and mobile devices
- **Sidebar Controls**: Easy access to all configuration options
- **Real-time Feedback**: Loading spinners, success/error messages
- **Session Persistence**: Maintains state across interactions

### Interactive Elements
- **Dropdown Menus**: Model selection, genre, age group
- **Sliders**: Temperature and token count control
- **Action Buttons**: Generate, search, image creation, TTS
- **Content Display**: Formatted output with copy functionality
- **Audio Player**: Built-in audio playback for generated speech

## 📱 Usage Examples

### Generate a Story
1. Select "Story" as content type
2. Choose genre (e.g., "Fantasy")
3. Select age group (e.g., "Children (5-12)")
4. Enter prompt: "A story about a brave little dragon"
5. Click "Generate Story"

### Web Search
1. Enter search query: "latest space exploration news"
2. Click "Web Search"
3. View filtered, safe search results

### Image Generation
1. Generate a story first
2. Click "Generate Image"
3. View AI-generated image based on story content

### Text-to-Speech
1. Generate content or enter text
2. Click "Text to Speech"
3. Listen to audio playback

## 🔍 Troubleshooting

### Common Issues

1. **Model Unavailable Error**
   - Check if API key is valid
   - Try switching to a different model
   - Verify API quota/billing

2. **Content Filtered**
   - Review input for sensitive keywords
   - Try rephrasing the prompt
   - Check content guidelines

3. **Search Not Working**
   - Verify SerpAPI key configuration
   - Check search query for safety violations
   - Review API quota

### Debug Mode
Streamlit automatically provides detailed error logging. Check the terminal output for debugging information.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT models and DALL-E
- Groq for fast LLM inference
- Google for Gemini models
- SerpAPI for web search capabilities
- React and Flask communities

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation
3. Create an issue in the repository

---

**Built with ❤️ using Python, Streamlit, and AI**
