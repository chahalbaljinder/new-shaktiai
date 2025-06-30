@echo off
echo Starting SHAKTI-AI Application...
echo.

echo Starting Python Backend Service...
start cmd /k "cd /d %~dp0 && python -m uvicorn backend_service:app --host 0.0.0.0 --port 8000 --reload"

echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo Starting Next.js Frontend...
start cmd /k "cd /d %~dp0shakti-ai-nextjs && npm run dev"

echo.
echo Both services are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3001
echo.
echo Press any key to exit...
pause >nul