"""
Project structure generator for AI Capstone Project
Run this script to automatically create all folders and files
"""
import os
from pathlib import Path

def create_structure():
    """Create the complete project structure"""
    
    # Define directory structure
    directories = [
        "phase1-foundation/config",
        "phase1-foundation/data/raw",
        "phase1-foundation/data/processed",
        "phase1-foundation/data/faqs",
        "phase1-foundation/rag-pipeline",
        "phase1-foundation/mini-projects/faq-assistant",
        "phase1-foundation/mini-projects/youtube-summarizer",
        "phase1-foundation/mini-projects/docs-assistant",
        "phase1-foundation/tests",
        "phase2-agents",
        "phase3-evaluation",
        "phase4-coding-agent",
        "phase5-production",
        "phase6-capstone",
        "shared/config",
        "shared/utils",
        "docs/daily-progress",
    ]
    
    # Create directories
    print("Creating directory structure...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {directory}")
    
    # Create __init__.py files
    init_files = [
        "phase1-foundation/__init__.py",
        "phase1-foundation/rag-pipeline/__init__.py",
        "phase1-foundation/mini-projects/__init__.py",
        "shared/__init__.py",
        "shared/config/__init__.py",
        "shared/utils/__init__.py",
    ]
    
    print("\nCreating __init__.py files...")
    for init_file in init_files:
        Path(init_file).touch()
        print(f"  ✓ {init_file}")
    
    # Create requirements.txt
    print("\nCreating requirements.txt...")
    requirements = """# Core Dependencies
openai==1.54.0
python-dotenv==1.0.0

# Vector Database
qdrant-client==1.11.3

# Document Processing
langchain==0.3.7
langchain-community==0.3.5
langchain-openai==0.2.5
pypdf==5.1.0
python-docx==1.1.2

# Data Processing
numpy==1.26.4
pandas==2.2.3

# YouTube Transcript
youtube-transcript-api==0.6.2

# Web Framework
fastapi==0.115.4
uvicorn==0.32.0

# Testing
pytest==8.3.3
pytest-asyncio==0.24.0

# Utilities
tiktoken==0.8.0
beautifulsoup4==4.12.3
requests==2.32.3
"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements)
    print("  ✓ requirements.txt")
    
    # Create .env template
    print("\nCreating .env template...")
    env_template = """# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
EMBEDDING_MODEL=text-embedding-3-small

# Qdrant Configuration
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=capstone_docs

# Application Settings
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
TEMPERATURE=0.7
"""
    
    with open(".env", "w") as f:
        f.write(env_template)
    print("  ✓ .env")
    
    # Create .gitignore
    print("\nCreating .gitignore...")
    gitignore = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Data
*.csv
*.json
*.pkl
phase1-foundation/data/raw/*
phase1-foundation/data/processed/*
!phase1-foundation/data/raw/.gitkeep
!phase1-foundation/data/processed/.gitkeep

# Logs
*.log
logs/

# Qdrant
qdrant_storage/

# OS
.DS_Store
Thumbs.db
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore)
    print("  ✓ .gitignore")
    
    # Create .gitkeep files for empty directories
    gitkeep_files = [
        "phase1-foundation/data/raw/.gitkeep",
        "phase1-foundation/data/processed/.gitkeep",
        "phase1-foundation/data/faqs/.gitkeep",
        "docs/daily-progress/.gitkeep",
    ]
    
    print("\nCreating .gitkeep files...")
    for gitkeep in gitkeep_files:
        Path(gitkeep).touch()
        print(f"  ✓ {gitkeep}")
    
    print("\n" + "="*50)
    print("✅ Project structure created successfully!")
    print("="*50)
    print("\nNext steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Run: setup.bat (to install dependencies)")
    print("3. Copy the Python code files from the documentation")
    print("4. Run: python phase1-foundation/test_rag_pipeline.py")
    print("\n")

if __name__ == "__main__":
    create_structure()