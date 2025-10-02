#!/usr/bin/env python3
"""
Test script to verify Gemini API connection and available models
"""

import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

def test_gemini_connection():
    """Test Gemini API connection and list available models"""
    
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in .env file")
        return False
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        print("✅ Gemini API configured successfully")
        
        # List available models
        print("\n🔍 Fetching available models...")
        models = genai.list_models()
        
        print("\n📋 Testing Free Tier Gemini models:")
        from config import Config
        
        free_tier_models = Config.GEMINI_MODELS
        working_models = []
        
        for model_name in free_tier_models:
            try:
                print(f"  🧪 Testing {model_name}...")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Say hello in one word.")
                print(f"    ✅ {model_name} - Response: {response.text}")
                working_models.append(model_name)
            except Exception as e:
                print(f"    ❌ {model_name} - Error: {e}")
        
        if working_models:
            print(f"\n🎉 Gemini API is working correctly!")
            print(f"Working free tier models: {', '.join(working_models)}")
            return True
        else:
            print(f"\n❌ No free tier models are working")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        return False

def main():
    print("🤖 Testing Gemini API Connection")
    print("=" * 40)
    
    if test_gemini_connection():
        print("\n✅ All tests passed! Gemini is ready to use.")
    else:
        print("\n❌ Tests failed. Please check your API key and try again.")
        print("\nTo get a Google API key:")
        print("1. Go to https://makersuite.google.com/app/apikey")
        print("2. Create a new API key")
        print("3. Add it to your .env file as GOOGLE_API_KEY=your_key_here")

if __name__ == "__main__":
    main()
