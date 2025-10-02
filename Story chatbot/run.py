#!/usr/bin/env python3
"""
Story Chatbot - Streamlit Application Runner
Run this file to start the Streamlit application
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if all required files and dependencies are present"""
    required_files = [
        'streamlit_app.py',
        'config.py',
        'requirements.txt',
        'services/llm_service.py',
        'services/content_filter.py',
        'services/web_search_service.py',
        'services/image_service.py',
        'services/tts_service.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    return True

def check_python_dependencies():
    """Check if Python dependencies are installed"""
    try:
        import streamlit
        import groq
        import google.generativeai
        import openai
        import requests
        from gtts import gTTS
        print("Python dependencies are installed")
        return True
    except ImportError as e:
        print(f"Missing Python dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has required keys"""
    env_file = Path('.env')
    if not env_file.exists():
        print(".env file not found")
        print("Please create a .env file with your API keys:")
        print("OPENAI_API_KEY=your_key_here")
        print("GROQ_API_KEY=your_key_here")
        print("GOOGLE_API_KEY=your_key_here")
        print("SERPAPI_KEY=your_key_here")
        return False
    
    # Read and check env file
    with open('.env', 'r') as f:
        content = f.read()
        
    required_keys = ['OPENAI_API_KEY', 'GROQ_API_KEY', 'GOOGLE_API_KEY', 'SERPAPI_KEY']
    missing_keys = []
    
    for key in required_keys:
        if key not in content or f"{key}=your_" in content:
            missing_keys.append(key)
    
    if missing_keys:
        print("Please configure the following API keys in your .env file:")
        for key in missing_keys:
            print(f"   - {key}")
        print("\nNote: The application will still run but some features may not work.")
    
    return True

def main():
    """Main function to run the Streamlit app"""
    print("Story Chatbot - Streamlit Application Runner")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\nPlease ensure all required files are present")
        return
    
    if not check_python_dependencies():
        return
    
    check_env_file()
    
    print("\nStarting Story Chatbot...")
    print("The app will open in your default browser")
    print("Press Ctrl+C to stop the application")
    print()
    
    # Run streamlit app
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\nStory Chatbot stopped. Goodbye!")
    except Exception as e:
        print(f"Error running Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
