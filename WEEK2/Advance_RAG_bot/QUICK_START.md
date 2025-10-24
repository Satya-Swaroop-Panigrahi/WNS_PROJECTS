# 🚀 Quick Start Guide - Advanced RAG Chatbot

## Prerequisites
- Python 3.9+
- API keys for your chosen LLM providers

## 🎯 3-Step Setup

### Step 1: Install Dependencies

**Option A: Full Installation (with observability)**
```bash
# Backend dependencies
cd backend
pip install -r requirements.txt

# Frontend dependencies  
cd ../frontend
pip install -r requirements.txt
```

**Option B: Minimal Installation (without observability)**
```bash
# Backend dependencies (minimal)
cd backend
pip install -r requirements-minimal.txt

# Frontend dependencies  
cd ../frontend
pip install -r requirements.txt
```

**Option C: Windows Installation (if you get compilation errors)**
```bash
# Backend dependencies (Windows-compatible)
cd backend
pip install -r requirements-windows.txt

# Frontend dependencies  
cd ../frontend
pip install -r requirements.txt
```

### Step 2: Configure API Keys
Create a `.env` file in the root directory:
```env
# At minimum, add one LLM provider
GEMINI_API_KEY=your_gemini_api_key_here
# OR
GROQ_API_KEY=your_groq_api_key_here
# OR  
COHERE_API_KEY=your_cohere_api_key_here

# Optional: Internet search
SERPER_API_KEY=your_serper_api_key_here
```

### Step 3: Start the Application

**Option A: Using Python Scripts**
```bash
# Terminal 1 - Backend
cd backend
python run_server.py

# Terminal 2 - Frontend  
cd frontend
python run_app.py
```

**Option B: Using Batch Files (Windows)**
```bash
# Double-click these files:
start_backend.bat
start_frontend.bat
```

**Option C: Manual Commands**
```bash
# Backend
cd backend/app
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend  
streamlit run app.py --server.port 8501
```

## 🌐 Access the Application
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔧 Troubleshooting

### Backend Won't Start
- **Test imports first**: `python test_imports.py`
- Check if port 8000 is available
- Verify all dependencies installed: `pip install -r requirements-minimal.txt`
- Check API keys in `.env` file

### Import Errors
```bash
# Test what's missing
cd backend
python test_imports.py

# Install minimal requirements if needed
pip install -r requirements-minimal.txt
```

### Windows Compilation Errors
If you get errors like "Microsoft Visual C++ 14.0 or greater is required":
```bash
# Use Windows-compatible requirements
cd backend
pip install -r requirements-windows.txt
```

**Alternative: Install Visual Studio Build Tools**
1. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install "C++ build tools" workload
3. Then try: `pip install -r requirements.txt`

### Frontend Won't Start  
- Check if port 8501 is available
- Ensure backend is running on port 8000
- Verify Streamlit installation: `pip install streamlit`

### Import Errors
- Make sure you're in the correct directory
- Check Python path and virtual environment
- Verify all dependencies are installed

## 🎉 You're Ready!
Once both servers are running, open http://localhost:8501 in your browser to start using the Advanced RAG Chatbot!

## 📚 Next Steps
- Upload documents to chat with
- Configure your preferred LLM
- Try different RAG variants
- Explore the advanced features
