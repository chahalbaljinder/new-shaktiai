@echo off
echo 🔍 SHAKTI-AI Authentication Debug
echo ===================================
echo.

cd /d "%~dp0"

echo 🧹 Step 1: Clearing any existing cookies/cache...
echo You should:
echo 1. Open browser Developer Tools (F12)
echo 2. Go to Application/Storage tab
echo 3. Clear all cookies for localhost:3000
echo 4. Clear localStorage and sessionStorage
echo.

echo 🚀 Step 2: Starting development server...
echo Watch the console logs for authentication debug info
echo.

npm run dev
