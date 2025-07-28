@echo off
echo 🚀 SHAKTI-AI Development Setup
echo ================================

cd /d "%~dp0"

if not exist "package.json" (
    echo ❌ Error: Please run this script from the shakti-ai-nextjs directory
    pause
    exit /b 1
)

if not exist "node_modules" (
    echo 📦 Installing dependencies...
    call npm install
)

echo 🛠️  Initializing database...
call npm run init-db

if %errorlevel% equ 0 (
    echo.
    echo ✅ Database initialized successfully!
    echo.
    echo 🧪 Test Login Credentials:
    echo Email: test@example.com
    echo Password: test123
    echo.
    echo 🌐 Starting development server...
    call npm run dev
) else (
    echo.
    echo ❌ Database initialization failed. Please check your PostgreSQL connection.
    echo Make sure PostgreSQL is running and the credentials in .env.local are correct.
    pause
)
