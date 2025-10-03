@echo off
echo 🤖 Story Chatbot - Starting Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo ⚠️  .env file not found
    echo Running setup script first...
    python setup.py
    echo.
    echo Please edit .env file with your API keys, then run this script again
    pause
    exit /b 1
)

REM Run the application
python run.py

pause
