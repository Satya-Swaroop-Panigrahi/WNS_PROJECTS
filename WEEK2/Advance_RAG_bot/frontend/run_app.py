#!/usr/bin/env python3
"""
Frontend startup script for Advanced RAG Chatbot
"""
import subprocess
import sys
import os

def main():
    print("Starting Advanced RAG Chatbot Frontend...")
    print("Frontend will be available at: http://localhost:8501")
    print("Make sure the backend is running on http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Run streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ])

if __name__ == "__main__":
    main()
