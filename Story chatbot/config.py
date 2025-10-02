import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    SERPAPI_KEY = os.getenv('SERPAPI_KEY')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Content Filtering
    SENSITIVE_KEYWORDS = [
        'violence', 'explicit', 'hate', 'discrimination', 'terrorism',
        'self-harm', 'illegal', 'harmful', 'dangerous'
    ]
    
    # Supported Genres
    GENRES = [
        'Adventure', 'Fantasy', 'Mystery', 'Romance', 'Sci-Fi', 
        'Horror', 'Comedy', 'Drama', 'Thriller', 'Children'
    ]
    
    # Age Groups
    AGE_GROUPS = [
        'Children (5-12)', 'Teen (13-17)', 'Young Adult (18-25)', 
        'Adult (26-50)', 'Senior (50+)'
    ]
    
    # Supported Models (Free Tier Only) - Tested and Working
    GROQ_MODELS = [
        'llama-3.1-8b-instant',  # Fast and efficient
        'gemma2-9b-it'           # Google's Gemma model
    ]
    
    OPENAI_MODELS = [
        'gpt-3.5-turbo'  # Free tier: $5 credit for new users
    ]
    
    # Gemini models - Updated for Gemini 2.5 API
    GEMINI_MODELS = [
        'gemini-2.5-flash',        # Balanced model with 1M token context
        'gemini-2.5-flash-lite',   # Cost-efficient, high-throughput
        'gemini-2.5-pro',          # Most powerful for complex reasoning
        'gemini-2.0-flash',        # Experimental multimodal model
        'gemini-2.0-flash-lite'    # Experimental lite version
    ]
