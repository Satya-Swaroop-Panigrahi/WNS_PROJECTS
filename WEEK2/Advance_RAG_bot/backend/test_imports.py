#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""
import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_imports():
    """Test all critical imports"""
    try:
        print("🔍 Testing imports...")
        
        # Test basic imports
        print("✅ Basic imports...")
        import fastapi
        import uvicorn
        import logging
        
        # Test app imports
        print("✅ App imports...")
        from models.models import ChatMessage
        from services.llm_service import LLMService
        from services.rag_service import RAGFactory
        from services.guardrails import EnhancedGuardrailsService
        from services.memory import ConversationMemory
        from services.document_processor import DocumentProcessor
        from config import settings
        
        # Test main app
        print("✅ Main app import...")
        from main import app
        
        print("🎉 All imports successful!")
        print("✅ Backend is ready to run!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Try installing missing dependencies:")
        print("   pip install -r requirements-minimal.txt")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("\n🚀 You can now run: python run_server.py")
    else:
        print("\n🔧 Please fix the import errors first")
