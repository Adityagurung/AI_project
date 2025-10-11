@echo off
echo ========================================
echo AI Capstone Project - Quick Setup
echo ========================================

echo.
echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your OpenAI API key
echo 2. Run: venv\Scripts\activate
echo 3. Run: cd phase1-foundation
echo 4. Run: python test_rag_pipeline.py
echo.
pause