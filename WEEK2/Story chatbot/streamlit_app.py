import streamlit as st
import os
import tempfile
import base64
from typing import Dict, Any
from config import Config
from services.llm_service import LLMService
from services.web_search_service import WebSearchService
from services.content_filter import ContentFilter
from services.image_service import ImageService
from services.tts_service import TTSService

# Configure Streamlit page
st.set_page_config(
    page_title="🤖 Story Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .content-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = ''
if 'generated_image' not in st.session_state:
    st.session_state.generated_image = ''
if 'search_results' not in st.session_state:
    st.session_state.search_results = []

# Initialize services
@st.cache_resource
def initialize_services():
    """Initialize all services once and cache them"""
    return {
        'llm_service': LLMService(),
        'web_search_service': WebSearchService(),
        'content_filter': ContentFilter(),
        'image_service': ImageService(),
        'tts_service': TTSService()
    }

services = initialize_services()

# Main header
st.markdown("""
<div class="main-header">
    <h1>🤖 Story Chatbot</h1>
    <p>AI-powered content generation with multiple LLM providers</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Content type selection
    content_type = st.selectbox(
        "Content Type",
        ["story", "joke", "chat"],
        format_func=lambda x: {"story": "📚 Story", "joke": "😄 Joke", "chat": "💬 Chat"}[x]
    )
    
    # LLM Provider selection
    provider = st.selectbox(
        "LLM Provider",
        ["groq", "openai", "gemini"]
    )
    
    # Show info for Gemini
    if provider == "gemini":
        st.info("💡 Gemini 2.5 models now available! Try Gemini 2.5 Flash for best performance.")
    
    # Model selection based on provider (Free tier models only)
    if provider == "groq":
        model = st.selectbox("Model", Config.GROQ_MODELS)
    elif provider == "openai":
        model = st.selectbox("Model", Config.OPENAI_MODELS)
    elif provider == "gemini":
        model = st.selectbox("Model", Config.GEMINI_MODELS)
    
    # Genre selection
    genre = st.selectbox("Genre", Config.GENRES)
    
    # Age group selection
    age_group = st.selectbox("Age Group", Config.AGE_GROUPS)
    
    # Temperature slider
    temperature = st.slider(
        "Temperature (Creativity)",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Higher values make output more creative and random"
    )
    
    # Max tokens slider
    max_tokens = st.slider(
        "Max Tokens",
        min_value=100,
        max_value=2000,
        value=500,
        step=50,
        help="Maximum length of generated content"
    )
    
    # API Status
    st.header("📊 API Status")
    
    # Check API keys
    api_status = {
        "Groq": "✅" if Config.GROQ_API_KEY else "❌",
        "OpenAI": "✅" if Config.OPENAI_API_KEY else "❌",
        "Gemini": "✅" if Config.GOOGLE_API_KEY else "❌",
        "SerpAPI": "✅" if Config.SERPAPI_KEY else "❌"
    }
    
    for api, status in api_status.items():
        st.write(f"{status} {api}")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("✍️ Input")
    
    # Text input
    user_input = st.text_area(
        "Enter your prompt:",
        placeholder="e.g., 'A story about a magical forest' or 'Tell me a joke about cats'",
        height=150
    )
    
    # Action buttons
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
    
    with col_btn1:
        generate_btn = st.button("🚀 Generate", type="primary", use_container_width=True)
    
    with col_btn2:
        search_btn = st.button("🔍 Web Search", use_container_width=True)
    
    with col_btn3:
        image_btn = st.button("🖼️ Generate Image", use_container_width=True)
    
    with col_btn4:
        tts_btn = st.button("🔊 Text to Speech", use_container_width=True)

with col2:
    st.header("📈 Quick Stats")
    
    # Display metrics
    col_metric1, col_metric2 = st.columns(2)
    
    with col_metric1:
        st.metric("Content Type", content_type.title())
    
    with col_metric2:
        st.metric("Model", model)

# Handle button clicks
if generate_btn:
    if not user_input.strip():
        st.error("Please enter a prompt!")
    else:
        with st.spinner("Generating content..."):
            try:
                result = services['llm_service'].generate_content(
                    prompt=user_input,
                    model_provider=provider,
                    model_name=model,
                    content_type=content_type,
                    genre=genre,
                    age_group=age_group,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                if result['success']:
                    st.session_state.generated_content = result['content']
                    st.success("Content generated successfully!")
                    
                    # Debug: Show what we received
                    st.info(f"Debug - Raw content length: {len(result['content'])} characters")
                    st.info(f"Debug - First 100 chars: {result['content'][:100]}...")
                else:
                    st.error(f"Error: {result['error']}")
                    
            except Exception as e:
                st.error(f"Error generating content: {str(e)}")

elif search_btn:
    if not user_input.strip():
        st.error("Please enter a search query!")
    else:
        with st.spinner("Searching..."):
            try:
                results = services['web_search_service'].search(user_input)
                st.session_state.search_results = results
                st.success(f"Found {len(results)} results!")
            except Exception as e:
                st.error(f"Search error: {str(e)}")

elif image_btn:
    content_to_image = st.session_state.generated_content or user_input
    if not content_to_image.strip():
        st.error("Please generate content first or enter an image prompt!")
    else:
        with st.spinner("Generating image..."):
            try:
                image_url = services['image_service'].generate_image(content_to_image)
                
                # Debug: Show what we got
                st.info(f"Debug - Image URL: {image_url}")
                
                if image_url and image_url != "https://via.placeholder.com/1024x1024/4A90E2/FFFFFF?text=Image+Generation+Unavailable":
                    st.session_state.generated_image = image_url
                    st.success("Image generated successfully!")
                else:
                    st.warning("Image generation unavailable. Please add OpenAI API key for image generation.")
                    
            except Exception as e:
                st.error(f"Image generation error: {str(e)}")

elif tts_btn:
    content_to_speech = st.session_state.generated_content or user_input
    if not content_to_speech.strip():
        st.error("Please generate content first or enter text for TTS!")
    else:
        with st.spinner("Converting to speech..."):
            try:
                audio_file = services['tts_service'].text_to_speech(content_to_speech)
                
                # Read audio file and create download link
                with open(audio_file, 'rb') as f:
                    audio_bytes = f.read()
                
                st.audio(audio_bytes, format='audio/mp3')
                st.success("Audio generated successfully!")
                
                # Clean up temp file
                services['tts_service'].cleanup_temp_file(audio_file)
                
            except Exception as e:
                st.error(f"TTS error: {str(e)}")

# Display results
if st.session_state.generated_content:
    st.header("📝 Generated Content")
    
    # Try multiple display methods
    try:
        # Method 1: Text area (preferred)
        st.text_area(
            "Generated Content:",
            value=st.session_state.generated_content,
            height=300,
            disabled=True,
            key="generated_content_display"
        )
    except:
        # Method 2: Markdown display
        st.markdown(st.session_state.generated_content)
    
    # Alternative: Raw content display
    with st.expander("🔍 View Raw Content"):
        st.code(st.session_state.generated_content)
    
    # Copy button
    if st.button("📋 Copy to Clipboard"):
        st.code(st.session_state.generated_content)

if st.session_state.generated_image:
    st.header("🖼️ Generated Image")
    
    # Debug: Show image URL
    st.info(f"Debug - Image URL: {st.session_state.generated_image}")
    
    try:
        # Try to display the image
        if st.session_state.generated_image.startswith('http'):
            st.image(st.session_state.generated_image, caption="AI Generated Image", use_column_width=True)
            
            # Download button for HTTP images
            try:
                import requests
                response = requests.get(st.session_state.generated_image)
                if response.status_code == 200:
                    st.download_button(
                        label="💾 Download Image",
                        data=response.content,
                        file_name="generated_image.png",
                        mime="image/png"
                    )
            except:
                st.warning("Could not download image")
        else:
            # For local file paths
            st.image(st.session_state.generated_image, caption="AI Generated Image", use_column_width=True)
            
    except Exception as e:
        st.error(f"Could not display image: {str(e)}")
        st.info("Image URL: " + st.session_state.generated_image)

if st.session_state.search_results:
    st.header("🔍 Search Results")
    
    for i, result in enumerate(st.session_state.search_results):
        with st.expander(f"Result {i+1}: {result['title']}"):
            st.write(result['snippet'])
            st.write(f"**Source:** {result.get('source', 'Unknown')}")
            st.write(f"**URL:** [Read more]({result['url']})")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🤖 Story Chatbot - Built with Streamlit, Python, and AI</p>
    <p>Features: Multi-LLM Support • Content Filtering • Image Generation • Text-to-Speech • Web Search</p>
</div>
""", unsafe_allow_html=True)
