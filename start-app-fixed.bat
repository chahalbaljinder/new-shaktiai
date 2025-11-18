@echo off
echo 🚀 Starting APEX Application
echo =============================

echo.
echo 📦 Step 1: Installing/updating dependencies...
cd /d "c:\Users\anjal\SHAKTI AII\new-shaktiai\shakti-ai-nextjs"
call npm install

echo.
echo 🔧 Step 2: Starting Next.js Development Server...
echo Frontend will be available at: http://localhost:3000 (or next available port)
echo.

start "APEX Frontend" cmd /k "cd /d \"c:\Users\anjal\SHAKTI AII\new-shaktiai\shakti-ai-nextjs\" && npm run dev"

echo.
echo ⏳ Waiting for frontend to start...
timeout /t 5 /nobreak > nul

echo.
echo 🐍 Step 3: Starting Python Backend Service...
echo Backend will be available at: http://localhost:8000
echo.

start "APEX Backend" cmd /k "cd /d \"c:\Users\anjal\SHAKTI AII\new-shaktiai\" && python backend_service.py"

echo.
echo ✅ Application Starting!
echo ========================
echo.
echo 🌐 Frontend: http://localhost:3000 (or check terminal for actual port)
echo 🔧 Backend:  http://localhost:8000
echo.
echo Both services are starting in separate windows.
echo You can close this window once both services are running.
echo.
pause
