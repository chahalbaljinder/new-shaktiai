#!/usr/bin/env pwsh

Write-Host "🚀 SHAKTI-AI Development Setup" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "package.json")) {
    Write-Host "❌ Error: Please run this script from the shakti-ai-nextjs directory" -ForegroundColor Red
    exit 1
}

# Install dependencies if node_modules doesn't exist
if (-not (Test-Path "node_modules")) {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    npm install
}

# Initialize database
Write-Host "🛠️  Initializing database..." -ForegroundColor Yellow
npm run init-db

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database initialized successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🧪 Test Login Credentials:" -ForegroundColor Cyan
    Write-Host "Email: test@example.com" -ForegroundColor White
    Write-Host "Password: test123" -ForegroundColor White
    Write-Host ""
    Write-Host "🌐 Starting development server..." -ForegroundColor Yellow
    npm run dev
} else {
    Write-Host "❌ Database initialization failed. Please check your PostgreSQL connection." -ForegroundColor Red
    Write-Host "Make sure PostgreSQL is running and the credentials in .env.local are correct." -ForegroundColor Yellow
}
