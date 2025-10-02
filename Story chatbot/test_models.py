#!/usr/bin/env python3
"""
Test script to check which models are actually available
"""

import os
import sys
from dotenv import load_dotenv

def test_groq_models():
    """Test Groq models"""
    print("Testing Groq Models...")
    try:
        from groq import Groq
        
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            print("  No Groq API key found")
            return []
        
        client = Groq(api_key=api_key)
        
        # Test models
        test_models = [
            'llama-3.1-8b-instant',
            'llama-3.1-70b-versatile', 
            'llama-3.1-405b-versatile',
            'mixtral-8x7b-32768',
            'gemma2-9b-it',
            'llama3-8b-8192'  # Old model for comparison
        ]
        
        working_models = []
        for model in test_models:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": "Say hello"}],
                    max_tokens=10
                )
                print(f"  [OK] {model} - Working")
                working_models.append(model)
            except Exception as e:
                print(f"  [X] {model} - Error: {str(e)[:100]}...")
        
        return working_models
        
    except ImportError:
        print("  Groq library not installed")
        return []
    except Exception as e:
        print(f"  Groq error: {e}")
        return []

def test_gemini_models():
    """Test Gemini models"""
    print("\nTesting Gemini Models...")
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("  No Google API key found")
            return []
        
        genai.configure(api_key=api_key)
        
        # Test models - Updated for Gemini 2.5
        test_models = [
            'gemini-2.5-flash',
            'gemini-2.5-flash-lite',
            'gemini-2.5-pro',
            'gemini-2.0-flash',
            'gemini-2.0-flash-lite',
            # Legacy models for comparison
            'gemini-1.5-flash',
            'gemini-1.5-pro',
            'gemini-1.0-pro'
        ]
        
        working_models = []
        for model in test_models:
            try:
                model_instance = genai.GenerativeModel(model)
                response = model_instance.generate_content("Say hello")
                print(f"  [OK] {model} - Working")
                working_models.append(model)
            except Exception as e:
                print(f"  [X] {model} - Error: {str(e)[:100]}...")
        
        return working_models
        
    except ImportError:
        print("  Google Generative AI library not installed")
        return []
    except Exception as e:
        print(f"  Gemini error: {e}")
        return []

def test_openai_models():
    """Test OpenAI models"""
    print("\nTesting OpenAI Models...")
    try:
        from openai import OpenAI
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("  No OpenAI API key found")
            return []
        
        client = OpenAI(api_key=api_key)
        
        # Test models
        test_models = [
            'gpt-3.5-turbo',
            'gpt-4',
            'gpt-4-turbo-preview',
            'gpt-4o-mini'
        ]
        
        working_models = []
        for model in test_models:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": "Say hello"}],
                    max_tokens=10
                )
                print(f"  [OK] {model} - Working")
                working_models.append(model)
            except Exception as e:
                print(f"  [X] {model} - Error: {str(e)[:100]}...")
        
        return working_models
        
    except ImportError:
        print("  OpenAI library not installed")
        return []
    except Exception as e:
        print(f"  OpenAI error: {e}")
        return []

def main():
    print("Model Availability Test")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Test all providers
    groq_models = test_groq_models()
    gemini_models = test_gemini_models()
    openai_models = test_openai_models()
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print(f"Working Groq models: {groq_models}")
    print(f"Working Gemini models: {gemini_models}")
    print(f"Working OpenAI models: {openai_models}")
    
    if groq_models or gemini_models or openai_models:
        print("\n[OK] You have working models available!")
    else:
        print("\n[X] No working models found. Check your API keys.")

if __name__ == "__main__":
    main()
