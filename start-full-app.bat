@echo off
echo 🚀 Starting SHAKTI-AI Full Stack Application
echo ==========================================

cd /d "%~dp0"

echo 🐍 Step 1: Starting Python Backend Service...
start "SHAKTI-AI Backend" cmd /k "cd /d "%~dp0" && python backend_service.py"

echo ⏳ Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo 🌐 Step 2: Starting Next.js Frontend...
cd shakti-ai-nextjs
start "SHAKTI-AI Frontend" cmd /k "npm run dev"

echo ✅ Both services starting!
echo.
echo 📍 Frontend: http://localhost:3000
echo 📍 Backend:  http://localhost:8000
echo.
echo 💬 Your chat with AI agents should now work!
echo.
pause
