#!/usr/bin/env python3
"""
Startup script for Railway deployment
"""
import os
import sys

def main():
    print("🚀 Railway Deployment: Starting SHAKTI-AI Backend")
    print(f"📍 Port: {os.environ.get('PORT', '8000')}")
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Working Directory: {os.getcwd()}")
    
    # Import and run the backend
    try:
        from shakti_backend import run_real_ai_backend
        run_real_ai_backend()
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
