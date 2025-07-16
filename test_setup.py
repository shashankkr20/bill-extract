#!/usr/bin/env python3
"""
Test script to verify Bill Information Extraction System setup
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required packages can be imported"""
    print("🔍 Testing package imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import google.generativeai
        print("✅ Google Generative AI imported successfully")
    except ImportError as e:
        print(f"❌ Google Generative AI import failed: {e}")
        return False
    
    try:
        import cv2
        print("✅ OpenCV imported successfully")
    except ImportError as e:
        print(f"❌ OpenCV import failed: {e}")
        return False
    
    try:
        import PIL
        print("✅ Pillow imported successfully")
    except ImportError as e:
        print(f"❌ Pillow import failed: {e}")
        return False
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy imported successfully")
    except ImportError as e:
        print(f"❌ SQLAlchemy import failed: {e}")
        return False
    
    try:
        import pandas
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        import reportlab
        print("✅ ReportLab imported successfully")
    except ImportError as e:
        print(f"❌ ReportLab import failed: {e}")
        return False
    
    return True

def test_environment():
    """Test environment variables"""
    print("\n🔍 Testing environment variables...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and api_key != "your_gemini_api_key_here":
        print("✅ Gemini API key found")
        return True
    else:
        print("❌ Gemini API key not found or not set")
        print("Please set GEMINI_API_KEY in your .env file")
        return False

def test_directories():
    """Test if required directories exist"""
    print("\n🔍 Testing directory structure...")
    
    required_dirs = ["backend", "templates", "static"]
    missing_dirs = []
    
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"✅ {dir_name}/ directory exists")
        else:
            print(f"❌ {dir_name}/ directory missing")
            missing_dirs.append(dir_name)
    
    return len(missing_dirs) == 0

def test_files():
    """Test if required files exist"""
    print("\n🔍 Testing required files...")
    
    required_files = [
        "main.py",
        "requirements.txt",
        "env.example",
        "README.md",
        "backend/__init__.py",
        "backend/database.py",
        "backend/models.py",
        "backend/gemini_service.py",
        "backend/image_processor.py",
        "backend/export_service.py",
        "templates/index.html"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def test_backend_imports():
    """Test if backend modules can be imported"""
    print("\n🔍 Testing backend module imports...")
    
    try:
        from backend.database import init_db, get_db
        print("✅ Backend database module imported")
    except ImportError as e:
        print(f"❌ Backend database import failed: {e}")
        return False
    
    try:
        from backend.models import BillExtraction
        print("✅ Backend models module imported")
    except ImportError as e:
        print(f"❌ Backend models import failed: {e}")
        return False
    
    try:
        from backend.gemini_service import GeminiService
        print("✅ Backend Gemini service imported")
    except ImportError as e:
        print(f"❌ Backend Gemini service import failed: {e}")
        return False
    
    try:
        from backend.image_processor import ImageProcessor
        print("✅ Backend image processor imported")
    except ImportError as e:
        print(f"❌ Backend image processor import failed: {e}")
        return False
    
    try:
        from backend.export_service import ExportService
        print("✅ Backend export service imported")
    except ImportError as e:
        print(f"❌ Backend export service import failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 Bill Information Extraction System - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Package Imports", test_imports),
        ("Environment Variables", test_environment),
        ("Directory Structure", test_directories),
        ("Required Files", test_files),
        ("Backend Modules", test_backend_imports)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\n🚀 To start the application, run:")
        print("   python run.py")
        print("\n   or")
        print("   python main.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("\n💡 Common solutions:")
        print("   1. Install missing packages: pip install -r requirements.txt")
        print("   2. Set your Gemini API key in .env file")
        print("   3. Check that all files are in the correct locations")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 