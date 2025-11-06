# Fix chunk loading errors script for Next.js
Write-Host "Fixing chunk loading errors..." -ForegroundColor Yellow
Write-Host ""

Write-Host "Step 1: Stopping any running Next.js processes..." -ForegroundColor Cyan
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host "Step 2: Clearing build cache..." -ForegroundColor Cyan
if (Test-Path ".next") { Remove-Item -Recurse -Force ".next" -ErrorAction SilentlyContinue }
if (Test-Path "node_modules\.cache") { Remove-Item -Recurse -Force "node_modules\.cache" -ErrorAction SilentlyContinue }

Write-Host "Step 3: Clearing npm cache..." -ForegroundColor Cyan
npm cache clean --force

Write-Host "Step 4: Reinstalling dependencies..." -ForegroundColor Cyan
npm install

Write-Host "Step 5: Starting development server..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting Next.js development server..." -ForegroundColor Green
Write-Host "Access your app at: http://localhost:3000" -ForegroundColor Green
Write-Host ""

# Start the development server
npm run dev