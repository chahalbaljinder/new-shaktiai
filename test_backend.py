"""
Simple test to check backend dependencies and start minimal service
"""

print("Testing SHAKTI-AI Backend Dependencies...")

try:
    print("1. Testing FastAPI import...")
    import fastapi
    print("✅ FastAPI imported successfully")
    
    print("2. Testing core.crew import...")
    import core.crew
    print("✅ core.crew imported successfully")
    
    print("3. Testing ask_shakti_ai function...")
    from core.crew import ask_shakti_ai
    print("✅ ask_shakti_ai function imported successfully")
    
    print("4. Starting minimal FastAPI server...")
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    
    app = FastAPI(title="SHAKTI-AI Backend Test")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:3001"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/")
    def read_root():
        return {"message": "SHAKTI-AI Backend is running!", "status": "ok"}
    
    @app.get("/test")
    def test_endpoint():
        return {"test": "Backend connection successful", "timestamp": "2025-07-29"}
    
    print("5. Starting server on http://localhost:8000")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Missing dependencies. Please install required packages.")
except Exception as e:
    print(f"❌ Error: {e}")
    print("Backend failed to start.")
