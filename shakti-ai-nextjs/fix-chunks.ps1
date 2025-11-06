# Comprehensive fix for Next.js chunk loading errors
Write-Host "=== SHAKTI-AI Chunk Loading Error Fix ===" -ForegroundColor Yellow
Write-Host ""

Write-Host "Step 1: Stopping all Node.js processes..." -ForegroundColor Cyan
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

Write-Host "Step 2: Comprehensive cache clearing..." -ForegroundColor Cyan
if (Test-Path ".next") { Remove-Item -Recurse -Force ".next" -ErrorAction SilentlyContinue }
if (Test-Path "node_modules\.cache") { Remove-Item -Recurse -Force "node_modules\.cache" -ErrorAction SilentlyContinue }
if (Test-Path ".next\cache") { Remove-Item -Recurse -Force ".next\cache" -ErrorAction SilentlyContinue }

Write-Host "Step 3: Clearing all caches..." -ForegroundColor Cyan
npm cache clean --force
if (Get-Command yarn -ErrorAction SilentlyContinue) { yarn cache clean }

Write-Host "Step 4: Updating dependencies..." -ForegroundColor Cyan
npm install

Write-Host "Step 5: Browser cache instructions..." -ForegroundColor Magenta
Write-Host "IMPORTANT: Please do the following in your browser:" -ForegroundColor Red
Write-Host "  1. Close ALL browser tabs with localhost:3000" -ForegroundColor White
Write-Host "  2. Clear browser cache (Ctrl+Shift+Delete)" -ForegroundColor White
Write-Host "  3. Or use Incognito/Private mode" -ForegroundColor White
Write-Host ""

Write-Host "Step 6: Starting development server with fixes..." -ForegroundColor Cyan
Write-Host ""
Write-Host "=== Starting SHAKTI-AI Development Server ===" -ForegroundColor Green
Write-Host "URL: http://localhost:3000" -ForegroundColor Green
Write-Host "Turbo: Disabled (to prevent chunk issues)" -ForegroundColor Yellow
Write-Host ""

# Start the development server with turbo disabled
npm run dev