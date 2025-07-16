#!/usr/bin/env python3
"""
Bill Information Extraction System - Startup Script
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if Gemini API key is set
if not os.getenv("GEMINI_API_KEY"):
    print("❌ Error: GEMINI_API_KEY environment variable is not set!")
    print("Please set your Gemini API key in the .env file.")
    print("You can get one from: https://makersuite.google.com/app/apikey")
    sys.exit(1)

# Create necessary directories
Path("uploads").mkdir(exist_ok=True)
Path("exports").mkdir(exist_ok=True)

print("🚀 Starting Bill Information Extraction System...")
print("📁 Created necessary directories")
print("🔑 Gemini API key found")

# Import and run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True,
        log_level="info"
    ) 