#!/usr/bin/env python3
"""
Story Chatbot Setup Script
This script helps you set up the environment and run the application
"""

import os
import sys
import subprocess
from pathlib import Path

def create_env_file():
    """Create .env file with template"""
    env_content = """# Story Chatbot Environment Variables
# Add your actual API keys below (Free Tier)

# OpenAI API Key (Free tier: $5 credit for new users)
# Get from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Groq API Key (Free tier: 30 requests/minute)
# Get from: https://console.groq.com/keys
GROQ_API_KEY=your_groq_api_key_here

# Google API Key (Free tier: 15 requests/minute)
# Get from: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=your_google_api_key_here

# SerpAPI Key (Free tier: 100 searches/month)
# Get from: https://serpapi.com/dashboard
SERPAPI_KEY=your_serpapi_key_here

# Note: You only need ONE API key to get started!
# The app will work with just one provider configured
"""
    
    if not Path('.env').exists():
        with open('.env', 'w') as f:
            f.write(env_content)
        print("Created .env file with template")
        print("Please edit .env file and add your actual API keys")
    else:
        print(".env file already exists")

def install_dependencies():
    """Install Python dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def check_requirements():
    """Check if all required files exist"""
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
    
    print("All required files present")
    return True

def main():
    """Main setup function"""
    print("Story Chatbot - Setup Script")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        print("\nPlease ensure all required files are present")
        return
    
    # Create .env file
    create_env_file()
    
    # Install dependencies
    if not install_dependencies():
        return
    
    print("\nSetup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file and add at least ONE API key")
    print("2. Run the application:")
    print("   python run.py")
    print("\nGet FREE API keys from:")
    print("- OpenAI: https://platform.openai.com/api-keys ($5 free credit)")
    print("- Groq: https://console.groq.com/keys (30 requests/min)")
    print("- Google: https://makersuite.google.com/app/apikey (15 requests/min)")
    print("- SerpAPI: https://serpapi.com/dashboard (100 searches/month)")
    print("\nTip: You only need ONE API key to get started!")

if __name__ == "__main__":
    main()
